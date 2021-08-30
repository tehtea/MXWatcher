import * as React from 'react';
import styled from 'styled-components/macro';
import { ReactComponent as PlusSign } from './assets/plus-sign.svg';
import VisibilityIcon from '@material-ui/icons/Visibility';
import EmailIcon from '@material-ui/icons/Email';
export function Logos() {
  return (
    <Wrapper>
      <VisibilityIcon className="logo" />
      <PlusSign className="sign" />
      <EmailIcon className="logo" />
    </Wrapper>
  );
}

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  color: ${p => p.theme.border};

  .logo {
    width: 4.5rem;
    height: 4.5rem;
  }

  .sign {
    width: 2rem;
    height: 2rem;
    margin: 0 2rem;
  }
`;
