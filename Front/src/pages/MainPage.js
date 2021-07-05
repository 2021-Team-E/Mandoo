import React from 'react';
import BlankTop from '../components/BlankTop';
import {useHistory} from 'react-router-dom';

const MainPage = () => {
    const history = useHistory();
    return(
        <div>
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <button onClick={() => history.push((`/`))}>메인페이지</button>
            <button onClick={() => history.push((`/signup`))}>회원가입</button>
            <button onClick={() => history.push((`/login`))}>로그인</button>
            <h1>메인페이지입니다.</h1>
        </div>
    )
}

export default MainPage