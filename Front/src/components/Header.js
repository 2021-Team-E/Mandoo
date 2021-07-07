import React,{useState} from 'react';
import {useHistory} from 'react-router-dom';

const Header = () => {
    const history = useHistory();
    const [isAuth, setIsAuth] = useState(window.localStorage.getItem('isAuth'))
    const logout = () => {
        window.localStorage.setItem("isAuth", 'false');
        setIsAuth(false);
    }
    return(
        <div>
            <button onClick={() => history.push((`/`))}>메인페이지</button>
            {window.localStorage.getItem('isAuth')=='true' ? 
                <button onClick = {logout}>로그아웃</button> : 
                <>
                <button onClick={() => history.push((`/signup`))}>회원가입</button>
                <button onClick={() => history.push((`/login`))}>로그인</button></>}
        </div>
    )
}
export default Header