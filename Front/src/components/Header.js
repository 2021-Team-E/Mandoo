import React,{useState} from 'react';
import logo from './logo.PNG';
import { Link } from 'react-router-dom';
import "./Header.css";


const Header = () => {
    const [isAuth, setIsAuth] = useState(window.localStorage.getItem('isAuth'))
    const logout = () => {
        window.localStorage.setItem("isAuth", 'false');
        setIsAuth(false);
    }
    return(
        <div className="nav">
            <div className="nav-logo">
                <Link to="/">
                <img src={logo} alt="logo" />
                </Link>
            </div>
            <div className="nav-items">
                <Link to="/" className="nav-item">Main </Link>
                {window.localStorage.getItem('isAuth')=='true' ? 
                <Link to="/" className="nav-item" onClick = {logout}>로그아웃</Link> : 
                <>
                <Link to="/signup" className="nav-item">Signup </Link>
                <Link to="/login" className="nav-item">Login </Link></>}
                <div className="nav-items-right"></div>
            </div>    
        </div>
    )
}
export default Header