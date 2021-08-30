"""
Adapted from https://github.com/ponyorm/pony/blob/orm/pony/orm/examples/estore.py
"""
from datetime import datetime
import csv

from pony.orm import *
import tldextract

import env
import secrets

if env.isLocal():
    db = Database('sqlite', 'emails.sqlite', create_db=True)
else:
    db = Database(
        provider='postgres',
        user=secrets.getSecret('cloud_sql_user'),
        password=secrets.getSecret('cloud_sql_password'),
        host=secrets.getSecret('cloud_sql_host'),
        database='postgres'
    )

class Company(db.Entity):
    companyName = Required(str, unique=True)
    domain = Optional(str, unique=False, nullable=True) # can be non-unique due to mergers, e.g. Lorillard and Reynolds. Optional too
    industry = Optional(str, unique=False, nullable=True)
    mxRecords = Set('MXRecord')

class MXRecord(db.Entity):
    id = PrimaryKey(int, auto=True)
    company = Required(Company)
    domain = Required(str, unique=False)
    createdAt = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    deletedAt = Optional(datetime)
    resolvedIPs = Optional('ResolvedMXRecordIP')

class ResolvedMXRecordIP(db.Entity):
    id = PrimaryKey(int, auto=True)
    mxRecord = Required(MXRecord)
    ip = Required(str)
    org = Required(str)
    hostname = Required(str)


sql_debug(True)
db.generate_mapping(create_tables=True)

@db_session
def populateCompanies():
    with open('fortune_1000_domains.txt') as csvfile:
        companyDomains = csv.reader(csvfile, delimiter=',')
        for row in companyDomains:
            companyName, _, industry, rawUrl, _ = row
            parsedUrl = tldextract.extract(rawUrl)
            domain = '{}.{}'.format(parsedUrl.domain, parsedUrl.suffix)
            Company(companyName=companyName, domain=domain, industry=industry)

@db_session
def populateCompaniesIfNotSeeded():
    if Company.select().first() is None:
        populateCompanies()

@db_session
def getCompanies(companyId=None, serialize=False):
    if companyId is not None:
        result = select(c for c in Company if c.id == companyId).order_by(lambda c: (c.industry , c.companyName))[:]
    else:
        result = select(c for c in Company).order_by(lambda c: (c.industry , c.companyName))[:]
    if serialize:
        result = list(map(lambda r: r.to_dict(), result))
    return result

@db_session
def getMxRecords(serialize=False):
    result = select(m for m in MXRecord)[:]
    if serialize:
        result = list(map(lambda r: r.to_dict(), result))
    return result
    
@db_session
def getResolvedMxRecordIPs(serialize=False):
    result = select(r for r in ResolvedMXRecordIP)[:]
    if serialize:
        result = list(map(lambda r: r.to_dict(), result))
    return result

@db_session
def getExistingMxRecordsForCompany(company):
    return select(record for record in MXRecord if record.company == company and record.deletedAt is None)[:]

@db_session
def getResolvedMxRecordIPsForCompany(company):
    return select(
        (resolvedRecord.org, mxRecord.createdAt, mxRecord.deletedAt)
        for resolvedRecord in ResolvedMXRecordIP for mxRecord in MXRecord
        if mxRecord.company == company and resolvedRecord.mxRecord == mxRecord
    )[:]

@db_session
def getTopServicesUsage(limit=10):
    return select(
        (resolvedRecord.org, count())
        for resolvedRecord in ResolvedMXRecordIP for mxRecord in MXRecord
        if mxRecord.deletedAt is None and resolvedRecord.mxRecord == mxRecord
    ).order_by(lambda org, count: desc(count))[:limit]

if __name__ == '__main__':
    with db_session:
        if Company.select().first() is None:
            populateCompanies()
    getCompanies()