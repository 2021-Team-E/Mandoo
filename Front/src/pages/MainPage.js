import React, {useState} from 'react';
import BlankTop from '../components/BlankTop';
import {useHistory} from 'react-router-dom';

const MainPage = () => {
    const history = useHistory();
    if(window.localStorage.getItem("isAuth")===null) {
        window.localStorage.setItem("isAuth", false);
    }
    const [isAuth, setIsAuth] = useState(window.localStorage.getItem("isAuth"))

    const logout = () => {
        window.localStorage.setItem("isAuth", false);
        setIsAuth(false);
    }

    return(
        <div>
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <button onClick={() => history.push((`/`))}>메인페이지</button>
            {isAuth ? 
                <button onClick = {logout}>로그아웃</button> : 
                <>
                <button onClick={() => history.push((`/signup`))}>회원가입</button>
                <button onClick={() => history.push((`/login`))}>로그인</button></>}
            <h1>메인페이지입니다.</h1>
        </div>
    )
}

export default MainPage