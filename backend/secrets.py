import os

from google.cloud import secretmanager

_secretManagerClient = secretmanager.SecretManagerServiceClient()

def getSecret(secretName):
    projectId = os.getenv('GOOGLE_CLOUD_PROJECT')
    secretPath = f'projects/{projectId}/secrets/{secretName}/versions/latest'
    response = _secretManagerClient.access_secret_version(request={'name': secretPath})
    return response.payload.data.decode('UTF-8')
