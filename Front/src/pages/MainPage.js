import React from 'react';
import Header from '../components/Header'
//import BlankTop from '../components/BlankTop';
//import {useHistory} from 'react-router-dom';
import {useState} from 'react';
import axios from 'axios';
import { USER_SERVER } from '../config';

// 테두리 만드는 css
const divBorder = {
    marginTop: "100px",
    marginBottom: "40px"
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
        const formData = new FormData()
        formData.append("image", fileImg)
        console.log(formData);
        try {
            const request = axios.post(`${USER_SERVER}/quizupload`, formData, {withCredentials:true})
            .then(function (response) {
                console.log(response);
            })
        }
        catch(e){
            console.log("error");
        }
    
    }
 //<BlankTop DesktopMargin='100' TabletMargin='3' MobileMargin='1'/>
    return(
        <div>
            <div className="nav">
                <Header/>
            </div>
            <div className="content" >
                <div style={divBorder}>
                    <img style={{"objectFit": "fill", "width": "150px", "height": "200px", "border": "solid 1px black"}} src={fileUrl} alt={fileUrl} />
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

        </div>
    );
}



export default MainPage