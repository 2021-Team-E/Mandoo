import styled from 'styled-components';
import BlankTop from '../components/BlankTop';
import Button from '../components/Button';
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import { USER_SERVER } from '../config';
import Header from '../components/Header';

const Fix = styled.div`
  min-height: 100vh;
  background-color: #f0f8ff;
  text-align: center;
`;

const Wrapper = styled.div`
  width: 50%;
  padding: 50px;
  display: inline-block;
  flex-direction: column;
  margin-top: 70px;
  margin-left: auto;
  margin-right: auto;
`;

const LargeP = styled.div`
  font-size: 30px;
  color: 'black';
  font-family: 'NanumSquare';
  margin-left: auto;
  margin-right: auto;
`;

const GrayCard = styled.div`
  width: 610px;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  font-family: 'NanumSquare';
  padding: 2vw 2vw 2vw 2vw;
  text-align: center;
`;
const Input = styled.input`
  width: 480px;
  height: 40px;
  background-color: #ffffff;
  margin-top: 20px;
  font-family: 'NanumSquare';
  font-size: 20px;
`;

const SignUp = () => {
  const history = useHistory();
  const [user, setUser] = useState({
    id: '',
    name: '',
    password1: '',
    password2: '',
  });
  const onInputChange = async (e) => {
    const { name, value } = e.target;
    setUser({
      ...user,
      [name]: value,
    });
  };
  const pwdCheck = (evt) => {
    if (user.id === '' || user.name === '' || user.password1 === '' || user.password2 === '') {
      alert('모든 항목의 값을 채워주세요.');
    } else if (user.password1 !== user.password2) {
      alert('비밀번호가 동일하지 않습니다.');
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
      const response = await axios.post(`${USER_SERVER}/api/v1/user/signup`, data);
      console.log(response);
      if (response.data.success) {
        history.push(`/`);
        alert('회원가입 되었습니다.');
      }
    } catch (error) {
      if (error.response.status === 403) {
        alert(error.response.data.message);
      }
    }
  };

  return (
    <Fix>
      <div>
        {/*<BlankTop DesktopMargin="3" TabletMargin="3" MobileMargin="1" />
         */}
        <Header />
      </div>

      <Wrapper>
        <BlankTop DesktopMargin="3" TabletMargin="3" MobileMargin="1" />
        <LargeP>회원가입</LargeP>
        <GrayCard>
          <form>
            <Input placeholder="  이름" name="name" onChange={onInputChange} />
            <Input placeholder="  아이디" name="id" onChange={onInputChange} />
            <Input
              style={{ fontFamily: 'Roboto' }}
              type="password"
              placeholder="  비밀번호"
              name="password1"
              onChange={onInputChange}
            />
            <Input
              style={{ fontFamily: 'Roboto' }}
              type="password"
              placeholder="  비밀번호 확인"
              name="password2"
              onChange={onInputChange}
            />
          </form>
          <div
            style={{
              clear: 'both',
              textAlign: 'center',
              marginTop: '30px',
              marginLeft: 'auto',
              marginRight: 'auto',
            }}
          >
            <Button
              width="100"
              font="20"
              background="#80B2E0"
              color="#ffffff"
              marginTop="30"
              marginRight="30"
              marginLeft="30"
              onClick={pwdCheck}
            >
              확인
            </Button>
            <Button
              width="100"
              font="20"
              background="#80B2E0"
              color="#ffffff"
              marginTop="30"
              marginRight="30"
              marginLeft="30"
              onClick={() => history.push(`/`)}
            >
              취소
            </Button>
          </div>
        </GrayCard>
      </Wrapper>
    </Fix>
  );
};
export default SignUp;
