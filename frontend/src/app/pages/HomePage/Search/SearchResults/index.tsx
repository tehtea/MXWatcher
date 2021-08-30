import React from 'react';
import styled from 'styled-components/macro';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Company, ParsedMXRecord } from 'types';
import { useMemo } from 'react';
import { Card, CardContent, CardHeader, Typography } from '@material-ui/core';
import { Alert } from '@material-ui/lab';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
  tableContainer: {
    marginTop: '5vh',
  },
});

export default function SearchResults({
  mxRecords,
  selectedCompany,
}: {
  mxRecords: ParsedMXRecord[];
  selectedCompany: Company | null;
}) {
  const classes = useStyles();

  const activeRecord = useMemo(() => {
    return mxRecords.find(record => !record.deletedAt);
  }, [mxRecords]);

  const inactiveRecords = useMemo(() => {
    return mxRecords.filter(record => record.deletedAt);
  }, [mxRecords]);

  return (
    <SearchResultsContainer>
      {!activeRecord && selectedCompany && (
        <Alert severity="error">
          Could not get an MXRecord for this company
        </Alert>
      )}
      {activeRecord && (
        <Card raised>
          <CardHeader title="Current Email Provider" />
          <CardContent>
            <Typography>Name: {activeRecord.provider}</Typography>
            <Typography>
              Usage First Recorded At: {activeRecord.createdAt}
            </Typography>
          </CardContent>
        </Card>
      )}
      {inactiveRecords.length > 0 && (
        <TableContainer
          component={props => (
            <Card raised {...props}>
              {props.children}
            </Card>
          )}
          className={classes.tableContainer}
        >
          <Table className={classes.table} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Previous Email Provider</TableCell>
                <TableCell align="right">Usage Started At</TableCell>
                <TableCell align="right">Usage Stopped At</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {inactiveRecords.map(oldRecord => (
                <TableRow key={oldRecord.provider}>
                  <TableCell component="th" scope="row">
                    {oldRecord.provider}
                  </TableCell>
                  <TableCell align="right">{oldRecord.createdAt}</TableCell>
                  <TableCell align="right">{oldRecord.deletedAt}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </SearchResultsContainer>
  );
}

const SearchResultsContainer = styled.div`
  margin: 5vh 0 5vh 0;
`;
