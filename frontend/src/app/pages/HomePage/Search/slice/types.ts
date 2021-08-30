import { Company, ParsedMXRecord } from 'types';

/* --- STATE --- */
export interface SearchFormState {
  companies: Company[];
  mxRecords: ParsedMXRecord[];
  selectedCompany: Company | null;
  searchError: string;
}
