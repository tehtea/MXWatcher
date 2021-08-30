def getProperProviderName(rawOrganizationName: str):
  topProvidersMappings = [
      ('proofpoint', 'Proofpoint'),
      ('microsoft', 'Mail 365'),
      ('mimecast', 'Mimecast'),
      ('cisco', 'Cisco'),
      ('avago', 'Avago'),
      ('google', 'GSuite'),
      ('amazon', 'AWS'),
  ]
  rawOrganizationNameLower = rawOrganizationName.lower()
  for substring, readableName in topProvidersMappings:
    if substring in rawOrganizationNameLower:
      return readableName
  return rawOrganizationName
