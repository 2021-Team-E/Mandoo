import React from "react"
import styled from "styled-components"

const StyledButton = styled.button`
  margin-top:${(props) => props.marginTop || 50}px;
  margin-right: ${(props) => props.marginRight || 80}px;
  height: ${(props) => props.height || 60}px ;
  width: ${(props) => props.width || 100}px ;
  border: 3px solid ${(props) => props.border|| "rgba( 255, 255, 255, 0 )"};
  color: ${(props) => props.color || "black"};
  background: ${(props) => props.background || "rgba( 255, 255, 255, 0 )"};
  font-size: ${props=> props.font || 0}px;
  font-weight: ${props=> props.weight || 'normal'};
  font-family: "NanumSquare";
  padding-right:5px;
  outline:none;
  border-radius: ${props => props.round || 0}px;
`

const Button = ({ children, border,margin, color,weight, background, font, width, round, marginTop, marginRight, ...rest  }) => {
  return (
    <StyledButton border={border} color={color} background={background} weight={weight}margin={margin} font={font} width={width} round={round} marginTop={marginTop} marginRight={marginRight} {...rest}>
      {children}
    </StyledButton>
  )
}
export default Button;