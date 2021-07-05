import styled from 'styled-components';
import BlankTop from '../components/BlankTop';
import Button from '../components/Button';
import React, {useState} from 'react';
import {useHistory} from 'react-router-dom';

const Fix =styled.div`
min-height:100vh;
background-color:  #ffffff;
text-align: center;
`;

const Wrapper = styled.div`
  width:50%;
  height: 100%;
  padding:30px;
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
    background-color: #DADBDB;
    margin-top: 50px;
    margin-bottom:50px;
    margin-left: auto;
    margin-right: auto;
    font-family: "NanumSquare";
    padding: 2vw 2vw 2vw 2vw;
    text-align: center;
`
const Input = styled.input`
    width: 480px;
    height: 50px;
    background-color: #EAEAEA;
    margin-top: 30px;
    font-family: "NanumSquare";
    font-size: 20px;
`

const SignUp = () => {
    const history = useHistory();
    const [user, setUser] = useState({
        name: '',
        username: '',
        password1: '',
        password2: '',
        phone: '',
        bank_account: ''
    });

    const onInputChange = async e => {
        const{name, value} = e.target;
        setUser({
            ...user,
            [name] : value
        })
    }
    return(
        <Fix>
            <div>
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <button onClick={() => history.push((`/`))}>메인페이지</button>
            <button onClick={() => history.push((`/signup`))}>회원가입</button>
            <button onClick={() => history.push((`/login`))}>로그인</button>
            </div>
            <Wrapper>
                <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
                <LargeP>회원가입</LargeP>
                <GrayCard>
                    <form onSubmit={()=>{console.log("제출")}}>
                        <Input placeholder="   이름" name="name"  onChange={onInputChange}/>
                        <Input placeholder="   아이디" name="username" onChange={onInputChange}/>
                        <Input style={{fontFamily:"Roboto"}}type="password" placeholder="   비밀번호" name="password1" onChange={onInputChange}/>
                        <Input style={{fontFamily:"Roboto"}}type="password" placeholder="   비밀번호 확인" name="password2" onChange={onInputChange}/>
                        <Button width='210' font="20" background="#3B8686" color="#FAECEC" marginTop="30" marginRight="20" type="submit">확인</Button>
                    </form>
                </GrayCard>
            </Wrapper>
        </Fix>
    );
}
export default SignUp;