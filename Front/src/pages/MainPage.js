import React, {useState} from 'react';
import BlankTop from '../components/BlankTop';
import Header from '../components/Header'

const MainPage = () => {
    if(window.localStorage.getItem("isAuth")===null) {
        window.localStorage.setItem("isAuth", 'false');
    }

    return(
        <div>
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <Header/>
            <h1>메인페이지입니다.</h1>
        </div>
    )
}

export default MainPage