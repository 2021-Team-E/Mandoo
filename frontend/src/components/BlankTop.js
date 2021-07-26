import React from 'react';
import styled from "styled-components";

const BlankDiv = styled.div`
  width: 100%;
  margin-top: ${(props) => props.DesktopMargin || 0}rem;
  @media only screen and (max-width: 1024px) {
    margin-top: ${(props) => props.TabletMargin || 0}rem;
  }
  @media only screen and (max-width: 768px) {
    margin-top: ${(props) => props.MobileMargin || 0}rem;
  }
`;

const BlankTop = ({ DesktopMargin, TabletMargin, MobileMargin }) => { //마진
  return (
    <BlankDiv
      DesktopMargin={DesktopMargin}
      TabletMargin={TabletMargin}
      MobileMargin={MobileMargin}
    ></BlankDiv>
  );
};

export default BlankTop;