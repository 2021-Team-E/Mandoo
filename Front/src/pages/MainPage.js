import React from 'react';
import Header from '../components/Header'
//import BlankTop from '../components/BlankTop';
//import {useHistory} from 'react-router-dom';
import {useState} from 'react';
import axios from 'axios';
import { USER_SERVER } from '../config';


// 테두리 만드는 css
const divBorder = {
    marginTop: "40px",
    marginBottom: "40px",
    border: "1px solid black",
    width: "150px",
    height: "200px"
    
};

const MainPage = (props) => {
    if(window.localStorage.getItem("isAuth")===null) {
        window.localStorage.setItem("isAuth", 'false');
    }
    //const history = useHistory();
    const [fileUrl, setFileUrl] = useState(null);
    const [fileImg, setFileImg] = useState(null);

    // 이미지 업로드 버튼 이벤트. 미리보기 
    function processImage(event) {
        const imageFile = event.target.files[0];
        const imageUrl = URL.createObjectURL(imageFile);
        
        setFileUrl(imageUrl)
        setFileImg(imageFile)
    }

    // 전송 버튼 클릭 이벤트
    const sendImage = () => {
        try {
            const request = axios.post(`${USER_SERVER}/getimg`, {fileImg}, {
                headers: { "Content-Type": `multipart/form-data` }
                }
            ).then(function (response) {console.log(response);})
            return {
                payload: request
            }
           
        }
        catch(e){
            console.log("error");
        }
    
    }
 //<BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
    return(
        <div>
            <div className="nav">
                <Header/>
            </div>
            <div className="content" style={{"float":"left"}}>
                <div style={divBorder}>
                    <img style={{"objectFit": "fill", "width": "150px", "height": "200px"}} 
                        src={fileUrl} alt={fileUrl} />
                </div>
                <div>
                    <input type='file'
                        accept='image/*'
                        name='question_img'
                        onChange={processImage}>
                    </input>
                    <button onClick={sendImage}>전송</button>
                </div>
            </div>
            
            <div className="table" align="right" style={{"float":"right", "margin-right":"100px","margin-top":"40px"}} >
                <table border ="1"  width="1000" height="500">
                    <thead>
                        <tr align="center">
                            <td width="100">문항번호</td>
                            <td width="150">문항내용</td>
                            <td width="100">참고내용</td>
                            <td width="70">선택01</td>
                            <td width="70">선택02</td>
                            <td width="70"> 선택03</td>
                            <td width="70">선택04</td>
                            <td width="50">정답</td>
                            <td width="50">점수</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                    </tbody>
                    
                </table>
            </div>
        </div>
    );
}



export default MainPage