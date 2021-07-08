import styled from 'styled-components';
import BlankTop from '../components/BlankTop';
import Button from '../components/Button';
import React, {useState} from 'react';
import { useEffect } from 'react';
import {useHistory} from 'react-router-dom';
import axios from 'axios';
import { USER_SERVER } from '../config';
import Header from '../components/Header'

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
`
const GrayCard = styled.div`
    width: 610px;
    background-color: #DADBDB;
    margin-top: 50px;
    margin-bottom:50px;
    margin-left: auto;
    margin-right: auto;
    font-family: "NanumSquare";
    padding: 2vw 2vw 1vw 2vw;
    text-align: center;
`

const Input = styled.input`
    width: 480px;
    height: 80px;
    background-color: #EAEAEA;
    margin-top: 50px;
    font-family: "NanumSquare";
    font-size: 20px;
`

const Login = () => {
    const history = useHistory();
    const [info, setInfo] = useState({
        id: '',
        password: ''
    });

    const clear = async () => {
        setInfo({ id:'', password:'' });
    }

    const onInputChange = async e => {
        const{name, value} = e.target;
        setInfo({
            ...info,
            [name] : value
        })
    }

    const formSubmit = async evt => {
        evt.preventDefault();
        try{
            const response = await axios.post(`${USER_SERVER}/login`, info);
            if(response.data.success){
                window.localStorage.setItem('isAuth', 'true');
                history.push(`/`);
            }
            else{
                alert("로그인 중 오류 발생!")
            }
        }
        catch{
            alert("로그인 중 오류 발생!")
        }
    }

    useEffect(() => {}, [info]);

    return(
        <Fix>
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <Header/>
            <Wrapper>
                <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
                <LargeP>로그인</LargeP>
                <GrayCard>
                    <LargeP style={{color:"#3B8686", display:"inline-block"}}>아이디</LargeP>
                    <LargeP style={{display:"inline-block"}}>를 통한 로그인</LargeP>
                    <form>
                        <Input placeholder="   아이디" name='id' value={info.id} onChange={onInputChange}/>
                        <Input style={{fontFamily:"Roboto"}}type="password" placeholder="   비밀번호" name='password' value={info.password} onChange={onInputChange}/>
                        <Button width='210' font="20" background="#3B8686" color="#FAECEC" marginRight="20" type="submit" onClick={formSubmit}>로그인</Button>
                        <Button width='210' font="20" background="#042525" color="#FAECEC" marginRight="0" onClick={clear}>취소</Button>
                        <Button width='210' font="20" background="#DADBDB" color="#000000" marginTop="10" marginRight="0" onClick={() => history.push(`/signup`)}>회원가입</Button>
                    </form>
                </GrayCard>
            </Wrapper>
        </Fix>
    );
}
export default Login;