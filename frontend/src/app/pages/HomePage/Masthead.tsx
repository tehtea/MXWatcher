import styled from 'styled-components/macro';
import { Logos } from './Logos';
import { Title } from './components/Title';
import { Lead } from './components/Lead';
import { WEBSITE_TITLE, WEBSITE_DESCRIPTION } from '../../../constants';

export function Masthead() {
  return (
    <Wrapper>
      <Logos />
      <Title>{WEBSITE_TITLE}</Title>
      <Lead>{WEBSITE_DESCRIPTION}</Lead>
    </Wrapper>
  );
}

const Wrapper = styled.main`
  height: max(25vh, 280px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;
