import React from 'react';
import BlankTop from '../components/BlankTop';
import {useHistory} from 'react-router-dom';
import {useState} from 'react';
import axios from 'axios';
import { USER_SERVER } from '../config';

const border = {
    marginTop: "40px",
    marginBottom: "40px",
    border: "1px solid black",
    width: "150px",
    height: "200px"
};


const MainPage = (props) => {
    
    const history = useHistory();
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
    const sendImage = (event) => {
        try {
            const request = axios.post(`${USER_SERVER}/getimg`, {fileImg})
            .then(function (response) {console.log(response);})
            return {
                payload: request
            }
        }
        catch(e){
            console.log("error");
        }
    
    }
 
    return(
        <div>
            <div className="nav">
                
            </div>
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <button onClick={() => history.push((`/`))}>메인페이지</button>
            <button onClick={() => history.push((`/signup`))}>회원가입</button>
            <button onClick={() => history.push((`/login`))}>로그인</button>
            <div style={border}>
                 <img style={{"objectFit": "fill", "width": "150px", "height": "200px"}} src={fileUrl} alt={fileUrl} />
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
    );
}



export default MainPage