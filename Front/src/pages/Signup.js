import styled from "styled-components";
import BlankTop from "../components/BlankTop";
import Button from "../components/Button";
import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { USER_SERVER } from "../config";
import Header from "../components/Header";

const Fix = styled.div`
  min-height: 100vh;
  background-color: #ffffff;
  text-align: center;
`;

const Wrapper = styled.div`
  width: 50%;
  height: 100%;
  padding: 30px;
  display: inline-block;
  flex-direction: column;
  margin-top: 10;
`;

const LargeP = styled.div`
  font-size: 40px;
  color: "black";
  font-family: "NanumSquare";
  margin-left: auto;
  margin-right: auto;
`;

const GrayCard = styled.div`
  width: 610px;
  background-color: #dadbdb;
  margin-top: 50px;
  margin-bottom: 50px;
  margin-left: auto;
  margin-right: auto;
  font-family: "NanumSquare";
  padding: 2vw 2vw 2vw 2vw;
  text-align: center;
`;
const Input = styled.input`
  width: 480px;
  height: 50px;
  background-color: #eaeaea;
  margin-top: 30px;
  font-family: "NanumSquare";
  font-size: 20px;
`;

const SignUp = () => {
  const history = useHistory();
  const [user, setUser] = useState({
    id: "",
    name: "",
    password1: "",
    password2: "",
  });
  const onInputChange = async (e) => {
    const { name, value } = e.target;
    setUser({
      ...user,
      [name]: value,
    });
  };
  const pwdCheck = (evt) => {
    if (
      user.id === "" ||
      user.name === "" ||
      user.password1 === "" ||
      user.password2 === ""
    ) {
      alert("모든 항목의 값을 채워주세요.");
    } else if (user.password1 !== user.password2) {
      alert("비밀번호가 동일하지 않습니다.");
    } else formSubmit(evt);
  };

  const formSubmit = async (evt) => {
    evt.preventDefault();
    const data = {
      id: user.id,
      name: user.name,
      password: user.password1,
    };
    try {
      const response = await axios.post(`${USER_SERVER}/api/signup`, data);
      console.log(response);
      if (response.data.success) history.push(`/`);
      else alert("회원가입이 완료되지 않았습니다!");
    } catch {
      console.log("error");
    }
  };

  return (
    <Fix>
      <div>
        <BlankTop DesktopMargin="3" TabletMargin="3" MobileMargin="1" />
        <Header />
      </div>

      <Wrapper>
        <BlankTop DesktopMargin="3" TabletMargin="3" MobileMargin="1" />
        <LargeP>회원가입</LargeP>
        <GrayCard>
          <form>
            <Input placeholder="   이름" name="name" onChange={onInputChange} />
            <Input placeholder="   아이디" name="id" onChange={onInputChange} />
            <Input
              style={{ fontFamily: "Roboto" }}
              type="password"
              placeholder="   비밀번호"
              name="password1"
              onChange={onInputChange}
            />
            <Input
              style={{ fontFamily: "Roboto" }}
              type="password"
              placeholder="   비밀번호 확인"
              name="password2"
              onChange={onInputChange}
            />
          </form>
          <Button
            width="210"
            font="20"
            background="#3B8686"
            color="#FAECEC"
            marginTop="30"
            marginRight="20"
            onClick={pwdCheck}
          >
            확인
          </Button>
        </GrayCard>
      </Wrapper>
    </Fix>
  );
};
export default SignUp;
