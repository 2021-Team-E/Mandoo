import React, { useMemo } from 'react';
import Header from '../components/Header'
import Table from '../components/Table'
//import BlankTop from '../components/BlankTop';
//import {useHistory} from 'react-router-dom';
import {useState} from 'react';
import axios from 'axios';
import { USER_SERVER } from '../config';
import Modal from '../components/Modals/Modal.js';
import "./table.css";

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

    //input data
    const columns = useMemo(
        () => [
            {
                accessor: "qid",
                Header: "문항번호",
            },
            {
                accessor: "title",
                Header: "문항내용",
            },
            {
                accessor: "script" ,
                Header: "참고내용",
            },
            {
                accessor: "choice1",
                Header: "선택01",
            },
            {
                accessor: "choice2",
                Header: "선택02",
            },
            {
                accessor: "choice3",
                Header: "선택03",
            },
            {
                accessor: "choice4",
                Header: "선택04",
            },
            {
                accessor: "choice5",
                Header: "선택05",
            },
            {
                accessor: "answer",
                Header: "정답",
            },
            {
                accessor: "score",
                Header: "점수",
            },
        ],
        []
    );
    const data = useMemo( 
        () =>
        Array(31)
            .fill()
            .map(()=>({
                //여기에 db랑 연결하는 코드 각각 작성
                qid: "0001",
                title: "다음 중 가장 적절한 것은?",
                choice1: "1번. 여인을 슬프고 우울해 보이게 그린 것을 보니~",
                choice2: "2번. 해바라기를 강조한 화면 구성을 보니~~",
                choice3:"3번. 해바라기의 노란색과 윤각의 빨간색을 대비한 것을 보니~~",
                choice4:"4번. 해바라기, 꽃병, 배경 등을 화려한 흰 색으로 그린 것을 보니~~",
                choice5:"5번. 해바라기 꽃병과 여인을 원근법에 어긋나게 그린 것을 보니~~",
                answer: 1,
                script: "독일 표현주의 화가인 키르히너의 <해바라기와 여인의 얼굴>은",
                image: "https://s3.ap-northeast-2.amazonaws.com/event-localnaeil/FileData/Article/202004/56c1b8c3-43e6-466b-8d66-6e56a770206c.jpg",
                score: "3점",
            })),
        []
    );


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
            const request = axios.post(`${USER_SERVER}/imageupload`, formData, {withCredentials:true})
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
            <div className="content">
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
            <div className="table" align="center" style={{"marginRight":"auto","marginTop":"30px","width": "80vw", "height": "70vh", "overflow":"auto", "border":"solid 2px black", "marginLeft":"auto"}} >
                <Table columns ={columns} data={data}/>
            </div>
            <div className="confirm" style={{"clear":"both"}}>
                    <button>확정</button>
                    <button>수정</button>
            </div>
        </div>
        
    );
}



export default MainPage