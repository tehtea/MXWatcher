import { Title } from '../components/Title';
import { Lead } from '../components/Lead';
import { TextField } from '@material-ui/core';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { useSearchFormSlice } from './slice';
import {
  selectCompanies,
  selectCompany,
  selectMxRecords,
} from './slice/selectors';
import { useSelector, useStore } from 'react-redux';
import { useMutation, useQuery } from 'react-query';
import { getCompanies, getRecordsForCompany } from 'services';
import { get, isNumber } from 'lodash';
import { useSnackbar } from 'notistack';
import SearchResults from './SearchResults';

export function Search() {
  const { enqueueSnackbar } = useSnackbar();
  const store = useStore();
  const searchFormSlice = useSearchFormSlice();
  const { isLoading: isLoadingCompanies } = useQuery(
    'getCompanies',
    getCompanies,
    {
      onSuccess: companies => {
        store.dispatch(searchFormSlice.actions.setCompanies(companies));
      },
      onError: error => {
        const errorMessage = get(
          error,
          'response.data.message',
          'We hit a snag while getting the list of companies',
        );
        enqueueSnackbar(errorMessage, {
          variant: 'error',
        });
        console.log('see getCompanies error: ', error);
      },
      refetchOnWindowFocus: false,
    },
  );
  const { mutate: initiateGetRecordsForCompany, isLoading: isLoadingRecords } =
    useMutation('getRecords', getRecordsForCompany, {
      onSuccess: mxRecords => {
        store.dispatch(searchFormSlice.actions.setMxRecords(mxRecords));
      },
      onError: error => {
        const errorMessage = get(
          error,
          'response.data.message',
          'We hit a snag while getting the MXRecords for a company',
        );
        enqueueSnackbar(errorMessage, {
          variant: 'error',
        });
        console.log('see getRecordsForCompany error: ', error);
      },
    });

  const companies = useSelector(selectCompanies);
  const mxRecords = useSelector(selectMxRecords);
  const selectedCompany = useSelector(selectCompany);

  return (
    <div id="search">
      <Title as="h2">Search</Title>
      <Lead>Find the history of email providers used by a company</Lead>
      <Autocomplete
        id="grouped-demo"
        options={companies}
        groupBy={option => option.industry}
        getOptionLabel={option => option.companyName}
        renderInput={params => (
          <TextField {...params} label="Company" variant="outlined" />
        )}
        value={selectedCompany}
        onChange={(event, company) => {
          const companyId = company?.id;
          if (company && companyId && isNumber(companyId)) {
            store.dispatch(searchFormSlice.actions.setSelectedCompany(company));
            initiateGetRecordsForCompany(companyId);
          }
        }}
      />
      <SearchResults mxRecords={mxRecords} selectedCompany={selectedCompany} />
    </div>
  );
}
