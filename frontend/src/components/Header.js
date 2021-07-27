import React, { useState, useEffect } from 'react';
import logo from './logo.PNG';
import { Link } from 'react-router-dom';
import './Header.css';
import axios from 'axios';
import { USER_SERVER } from '../config';
import { useHistory } from 'react-router';

const Header = () => {
  const [isAuth, setIsAuth] = useState(window.localStorage.getItem('isAuth'));
  const history = useHistory();
  useEffect(() => {}, [isAuth]);

  // 로그아웃
  const logout = async () => {
    const response = await axios.get(`${USER_SERVER}/api/v1/user/logout`);
    console.log(response);
    window.localStorage.setItem('isAuth', 'false');
    setIsAuth(false);
    history.push('/');
    alert('로그아웃 되었습니다.');
  };

  // navigation의 메뉴 누르면 각자 페이지로 이동.
  // 로고 누르면 메인페이지로 이동
  return (
    <div className="nav">
      <div className="nav-logo">
        <Link to="/">
          <img src={logo} alt="logo" />
        </Link>
      </div>
      <div className="nav-items">
        <Link to="/" className="nav-item">
          Main{' '}
        </Link>
        {window.localStorage.getItem('isAuth') === 'true' ? (
          <Link to="/" className="nav-item" onClick={logout}>
            Logout
          </Link>
        ) : (
          <>
            <Link to="/signup" className="nav-item">
              Signup{' '}
            </Link>
            <Link to="/login" className="nav-item">
              Login{' '}
            </Link>
          </>
        )}
        <div className="nav-items-right"></div>
      </div>
    </div>
  );
};
export default Header;
