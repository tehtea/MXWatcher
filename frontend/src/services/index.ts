import React from 'react';
import axios from 'axios';
import { Company, ParsedMXRecord, Usage } from 'types';

// credit: https://stackoverflow.com/questions/52702466/detect-react-reactdom-development-production-build/52857179#52857179
const ReactIsInDevelopmentMode = () => {
  return '_self' in React.createElement('div');
};

const BASE_URL = ReactIsInDevelopmentMode() ? 'http://localhost:5000' : '';

const http = axios.create({
  baseURL: BASE_URL,
});

export const getTopServicesUsage = async (): Promise<Usage[]> => {
  return http
    .get('/getTopServicesUsage')
    .then(({ data: { data: usages } }: { data: { data: Usage[] } }) => usages);
};

export const getCompanies = async (): Promise<Company[]> => {
  return http
    .get('/getCompanies')
    .then(
      ({ data: { data: companies } }: { data: { data: Company[] } }) =>
        companies,
    );
};

export const getRecordsForCompany = async (
  companyId: number,
): Promise<ParsedMXRecord[]> => {
  return http
    .get('/getRecordsForCompany', { params: { companyId } })
    .then(
      ({ data: { data: companies } }: { data: { data: ParsedMXRecord[] } }) =>
        companies,
    );
};

export const submitQuery = async (
  companyName: string,
): Promise<ParsedMXRecord[]> => {
  return axios.get('/getMXRecords', { params: { companyName } });
};
