"""
Reference:
https://github.com/ponyorm/pony/issues/32
"""
import os
import unittest
import tempfile
from unittest.mock import patch, call

from pony.orm.core import db_session

import crawler
import datastore


class TestCrawl(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    return super().setUpClass()

  def mockDB(self):
    from datastore import db
    from pony.orm import Database
    self.DBFileDescriptor, self.DBFilePath = tempfile.mkstemp()
    mockDB = Database(provider='sqlite', filename=self.DBFilePath)
    mockDB.entities = db.entities
    mockDB.generate_mapping(create_tables=True)
    db.provider = mockDB.provider
    db.schema = mockDB.schema
    self.db = db

  def tearDownMockDB(self):
    # self.db.stop()
    os.close(self.DBFileDescriptor)
    os.remove(self.DBFilePath)

  def setUp(self):
    self.mockDB()
    pass

  def tearDown(self):
    self.tearDownMockDB()
    pass

  @db_session
  def test_providerChange_addsNewMXRecord(self):
    sampleProofpointDomain = 'beaerospace.com'
    mockCompany = self.db.Company(
        companyName='DEBUG_INC_2', domain=sampleProofpointDomain, industry='DEBUG')
    crawler._crawlCompany(mockCompany)
    initialRecords = datastore.getResolvedMxRecordIPsForCompany(mockCompany)
    self.assertEqual(len(initialRecords), 1)
    # change domain to mock change in provider
    sampleMSDomain = 'transdigm.com'
    mockCompany.domain = sampleMSDomain
    crawler._crawlCompany(mockCompany)
    finalRecords = datastore.getResolvedMxRecordIPsForCompany(mockCompany)
    finalRecords.sort(key=lambda record: record[1])  # sort by createdAt ASC
    self.assertEqual(len(finalRecords), 2)
    self.assertIsNotNone(finalRecords[0][2])

  @db_session
  def test_noMXRecordFound_domainDeleted(self):
    domainWithNoMXRecord = 'phillips66.com'
    companyWithNoMXRecord = self.db.Company(
        companyName='DEBUG_INC_2', domain=domainWithNoMXRecord, industry='DEBUG')
    crawler._crawlCompany(companyWithNoMXRecord)
    mxRecords = datastore.getResolvedMxRecordIPsForCompany(
        companyWithNoMXRecord)
    self.assertEqual(len(mxRecords), 0)
    self.assertIsNone(companyWithNoMXRecord.domain)
