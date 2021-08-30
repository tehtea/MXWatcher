import * as React from 'react';
import styled from 'styled-components/macro';
import { Title } from '../components/Title';
import { Lead } from '../components/Lead';
import { Card, CardContent, CardHeader, Typography } from '@material-ui/core';
import { useQuery } from 'react-query';
import { getTopServicesUsage } from 'services';
import { useState } from 'react';
import { get } from 'lodash';
import { Usage } from 'types';
import { useSnackbar } from 'notistack';

export function Statistics() {
  const { enqueueSnackbar } = useSnackbar();
  const [usages, setUsages] = useState([] as Usage[]);
  const { isLoading } = useQuery('getTopServicesUsage', getTopServicesUsage, {
    onSuccess: newlyFetchedUsages => {
      setUsages(newlyFetchedUsages);
    },
    onError: error => {
      const errorMessage = get(
        error,
        'response.data.message',
        'We hit a snag while getting the statistics',
      );
      enqueueSnackbar(errorMessage, {
        variant: 'error',
      });
    },
    refetchOnWindowFocus: false,
  });
  return (
    <StatsContainer id="statistics">
      <Title as="h2">Overall Statistics</Title>
      <Lead>Top three commonly used mail providers / security solutions</Lead>
      <StatCards>
        {usages.map(usage => {
          return (
            <Card raised>
              <CardHeader title={`${usage.provider}`} />
              <CardContent>
                <Typography>{usage.usageRate}%</Typography>
              </CardContent>
            </Card>
          );
        })}
      </StatCards>
    </StatsContainer>
  );
}

const StatsContainer = styled.div`
  margin: 5vh 0 5vh 0;
`;

const StatCards = styled.div`
  display: flex;
  flex-direction: row;
  align-content: space-between;
  justify-content: space-between;
  margin: 0 0 0 0;
`;
