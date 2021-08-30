import { PayloadAction } from '@reduxjs/toolkit';
import { Company, ParsedMXRecord } from 'types';
import { createSlice } from 'utils/@reduxjs/toolkit';
import { useInjectReducer } from 'utils/redux-injectors';
import { SearchFormState } from './types';

export const initialState: SearchFormState = {
  companies: [],
  mxRecords: [],
  selectedCompany: null,
  searchError: '',
};

const slice = createSlice({
  name: 'companySearchForm',
  initialState,
  reducers: {
    setCompanies(state, action: PayloadAction<Company[]>) {
      state.companies = action.payload;
    },
    setMxRecords(state, action: PayloadAction<ParsedMXRecord[]>) {
      state.mxRecords = action.payload;
    },
    setSelectedCompany(state, action: PayloadAction<Company>) {
      state.selectedCompany = action.payload;
    },
    setSearchError(state, action: PayloadAction<any>) {
      state.searchError = action.payload;
    },
  },
});

export const { actions: searchFormActions, reducer } = slice;

export const useSearchFormSlice = () => {
  useInjectReducer({ key: slice.name, reducer: slice.reducer });
  return { actions: slice.actions };
};
