import React,{useState} from 'react';
import logo from './logo.PNG';
import { Link } from 'react-router-dom';

const Header = () => {
    const [isAuth, setIsAuth] = useState(window.localStorage.getItem('isAuth'))
    const logout = () => {
        window.localStorage.setItem("isAuth", 'false');
        setIsAuth(false);
    }
    return(
        <div>
                <img src={logo} alt="logo" />
                <Link to="/" >Main </Link>
            {window.localStorage.getItem('isAuth')=='true' ? 
                <button onClick = {logout}>로그아웃</button> : 
                <>
                <Link to="/signup" >Signup </Link>
                <Link to="/login" >Login </Link></>}
        </div>
    )
}
export default Header