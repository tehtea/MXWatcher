import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import { NavBar } from 'app/components/NavBar';
import { Masthead } from './Masthead';
import { PageWrapper } from 'app/components/PageWrapper';
import { WEBSITE_TITLE, WEBSITE_DESCRIPTION } from '../../../constants';
import { Statistics } from './Statistics';
import { Search } from './Search';

export function HomePage() {
  return (
    <>
      <Helmet>
        <title>{WEBSITE_TITLE}</title>
        <meta name="description" content={WEBSITE_DESCRIPTION} />
      </Helmet>
      <NavBar />
      <PageWrapper>
        <Masthead />
        <Statistics />
        <Search />
      </PageWrapper>
    </>
  );
}
