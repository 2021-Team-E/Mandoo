import React from 'react';
import Header from '../components/Header'
//import BlankTop from '../components/BlankTop';
//import {useHistory} from 'react-router-dom';
import {useState} from 'react';
import axios from 'axios';
import { USER_SERVER } from '../config';
import Modal from '../components/Modals/Modal.js';

// 테두리 만드는 css
const divBorder = {
    marginBottom: "40px"
};

const MainPage = (props) => {
    if(window.localStorage.getItem("isAuth")===null) {
        window.localStorage.setItem("isAuth", 'false');
    }
    //const history = useHistory();
    const [fileUrl, setFileUrl] = useState(null);
    const [fileImg, setFileImg] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);

    const openModal = () => {
        setModalOpen(true);
    }

    const closeModal = () => {
        setModalOpen(false);
    }

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
        <div style={{"backgroundColor":"#f0f8ff", "width":"100vw", "height":"100vh"}}>
            <div className="nav">
                <Header/>
            </div>
            <div className="content" style={{"float":"left"}}>
                <button onClick={openModal} style={{"marginTop":"100px"}}>모달창</button>
                <Modal open={modalOpen} close={closeModal}>
                    <div style={divBorder}>
                        <img style={{"objectFit": "fill", "width": "150px", "height": "200px", "border":"solid 1px black"}} 
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
                </Modal>
            </div>
            <div className="table" align="right" style={{"float":"right", "marginRight":"100px","marginTop":"100px"}} >
                <table border ="1"  width="1000" height="500" align="center">
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
                    <tbody align="center">
                        <tr>
                            <td><input style={{"width":"100px"}} type="text" /></td>
                            <td><input style={{"width":"150px"}} type="text" /></td>
                            <td><input style={{"width":"100px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"50px"}} type="text" /></td>
                            <td><input style={{"width":"50px"}} type="text" /></td>
                        </tr>
                        <tr>
                        <td><input style={{"width":"100px"}} type="text" /></td>
                            <td><input style={{"width":"150px"}} type="text" /></td>
                            <td><input style={{"width":"100px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"70px"}} type="text" /></td>
                            <td><input style={{"width":"50px"}} type="text" /></td>
                            <td><input style={{"width":"50px"}} type="text" /></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div className="confirm" style={{"clear":"both"}}>
                    <button>확정</button>
                    <button>수정</button>
            </div>
        </div>
        
    );
}



export default MainPage