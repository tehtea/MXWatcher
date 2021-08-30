from datetime import datetime
import logging

import dns.resolver
import ipinfo
from pony.orm import db_session

import datastore
import env
import secrets

_logger = logging.getLogger('App')

if env.isLocal():
  _ipInfoAccessToken = 'INSERT_YOUR_TOKEN_HERE'
else:
  _ipInfoAccessToken = secrets.getSecret('ipinfo_access_token')
_ipInfoHandler = ipinfo.getHandler(_ipInfoAccessToken)


def _getDomainRecords(domain):
  mxRecords = list(dns.resolver.resolve(domain, 'mx'))
  mxRecords.sort(key=lambda mxRecord: mxRecord.exchange.to_text())
  return mxRecords


@db_session
def _persistDomainRecord(mxRecord, company):
  mxRecordDomain = mxRecord.exchange.to_text()
  persistedMxRecord = datastore.MXRecord(
      company=company, domain=mxRecordDomain)
  possibleMxRecordIPs = list(dns.resolver.resolve(mxRecordDomain, 'A'))
  possibleMxRecordIPs.sort(key=lambda mxRecordIP: mxRecordIP.address)
  if len(possibleMxRecordIPs) == 0:
    _logger.warning(
        'Could not get IP info for mxRecordDomain: %s', mxRecordDomain)
    return
  mxRecordIP = possibleMxRecordIPs[0]
  mxRecordIP = mxRecordIP.address
  details = _ipInfoHandler.getDetails(mxRecordIP).all
  persistedMxIp = datastore.ResolvedMXRecordIP(\
    mxRecord=persistedMxRecord,\
      ip=details.get('ip', 'unknown'),\
        org=details.get('org', 'unknown'),\
          hostname=details.get('hostname', 'unknown'))


def _crawlCompany(company):
  domain = company.domain
  if domain is None:  # skip if domain has been erased prior
    return
  _logger.info('Crawling for: %s', domain)
  try:
    existingMxRecords = datastore.getExistingMxRecordsForCompany(company)
    potentialNewMxRecords = _getDomainRecords(domain)
    potentialNewMxRecord = potentialNewMxRecords[0]
    newMxRecordDomain = potentialNewMxRecord.exchange.to_text()
    recordIsNew = not any(map(
        lambda existingMxRecord: existingMxRecord.domain == newMxRecordDomain, existingMxRecords))
    if recordIsNew:
      _persistDomainRecord(potentialNewMxRecord, company)
      for oldRecord in existingMxRecords:
        oldRecord.deletedAt = datetime.now()
          
  except dns.resolver.NoAnswer:
    _logger.warning('Could not get MXRecord for domain: %s', domain)
    company.domain = None
    return
  except Exception as e:
    _logger.exception(e)
    _logger.warning(
        'Unexpected error while getting MXRecord for domain: %s', domain)
    return


@db_session
def crawl():
  _logger.info('Starting the crawling process')
  datastore.populateCompaniesIfNotSeeded()
  for company in datastore.getCompanies():
    _crawlCompany(company)

@db_session
def fetchFromDB():
  _logger.info('Fetching from DB')
  return {
      'companies': datastore.getCompanies(serialize=True),
      'mxRecords': datastore.getMxRecords(serialize=True),
      'resolvedMxRecordIPs': datastore.getResolvedMxRecordIPs(serialize=True),
  }


if __name__ == '__main__':
  crawl()
