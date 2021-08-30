import { RootState } from './RootState';

export type Usage = {
  provider: string;
  usageRate: number;
};

export type Company = {
  id: number;
  industry: string;
  companyName: string;
  domain: string;
};

export type ParsedMXRecord = {
  provider: string;
  createdAt: string;
  deletedAt: string;
};

export type { RootState };
