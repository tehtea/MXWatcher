import { createSelector } from '@reduxjs/toolkit';

import { RootState } from 'types';
import { initialState } from '.';

// First select the relevant part from the state
const selectDomain = (state: RootState) =>
  state.companySearchForm || initialState;

export const selectCompanies = createSelector(
  [selectDomain],
  searchFormState => searchFormState.companies,
);

export const selectMxRecords = createSelector(
  [selectDomain],
  searchFormState => searchFormState.mxRecords,
);

export const selectCompany = createSelector(
  [selectDomain],
  searchFormState => searchFormState.selectedCompany,
);
