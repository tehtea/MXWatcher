from collections import defaultdict
import sys
from http import HTTPStatus
import logging

from flask import Flask, render_template, request
from flask_cors import CORS

import crawler
import utils

# adapted from https://stackoverflow.com/questions/44209978/serving-a-front-end-created-with-create-react-app-with-flask
app = Flask('App', static_folder='build/static', template_folder='build')
CORS(app)
logger = logging.getLogger('App')


def setupLogger(logger):
  logger.setLevel(logging.INFO)
  consoleHandler = logging.StreamHandler(sys.stdout)
  consoleHandler.setLevel(logging.INFO)
  consoleHandler.setFormatter(
      logging.Formatter(
          '%(asctime)s %(levelname)s %(lineno)s %(funcName)s %(message)s'
      )
  )
  logger.addHandler(consoleHandler)


setupLogger(logger)


@app.route('/crawlMXRecords', methods=['GET'])
def crawlMXRecords():
  try:
    crawler.crawl()
    return ({'message': 'Crawled MXRecords successfully today!'}, HTTPStatus.OK)
  except Exception as error:
    logger.error(error)
    return ({'message': 'Unexcepted error while crawling MXRecords'}, HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/', methods=['GET'])
def welcome():
  return render_template('index.html')


@app.route('/fetchFromDB', methods=['GET'])
def fetchFromDB():
  data = crawler.fetchFromDB()
  return ({'data': data}, HTTPStatus.OK)


@app.route('/getCompanies', methods=['GET'])
def getCompanies():
  companies = crawler.datastore.getCompanies(serialize=True)
  return ({'data': companies}, HTTPStatus.OK)


@app.route('/getRecordsForCompany', methods=['GET'])
def getRecordsForCompany():
  companyId = request.args.get('companyId')
  company = crawler.datastore.getCompanies(companyId)[0]
  mxRecords = crawler.datastore.getResolvedMxRecordIPsForCompany(company)
  mxRecords = list(map(lambda r: {
      "provider": utils.getProperProviderName(r[0]),
      "createdAt": r[1],
      "deletedAt": r[2],
  }, mxRecords))
  return ({'data': mxRecords}, HTTPStatus.OK)


@app.route('/getTopServicesUsage', methods=['GET'])
def getTopServicesUsage():
  orgAndCount = crawler.datastore.getTopServicesUsage()
  providerAndUsageDict = defaultdict(int)
  for org, count in orgAndCount:
    provider = utils.getProperProviderName(org)
    providerAndUsageDict[provider] += count
  for provider in providerAndUsageDict:
    providerAndUsageDict[provider] /= 10  # convert to usage percentage
  providerAndUsage = [{'provider': key, 'usageRate': value}
                      for key, value in providerAndUsageDict.items()]
  providerAndUsage.sort(key=lambda payload: payload['usageRate'], reverse=True)
  providerAndUsage = providerAndUsage[:3]
  return ({'data': providerAndUsage}, HTTPStatus.OK)


if __name__ == '__main__':
  if crawler._ipInfoAccessToken == 'INSERT_YOUR_TOKEN_HERE':
    logger.error('Please provide a valid IPInfo token in `crawler.py`.')
    sys.exit(1)
  app.run('127.0.0.1', '5000', debug=True)
