import React, { useMemo } from "react";
import Header from "../components/Header";
import Table from "../components/Table";
//import BlankTop from '../components/BlankTop';
//import {useHistory} from 'react-router-dom';
import { useState, useEffect } from "react";

import axios from "axios";
import { USER_SERVER } from "../config";
import Modal from "../components/Modals/Modal.js";
import addImg from "./imgIcon.png";
import { useHistory } from "react-router-dom";
import { EditText} from "react-edit-text";


// 테두리 만드는 css
const divBorder = {
  marginBottom: "40px",
  position: "relation",
};

// 버튼관련 css
const btn = {
  marginTop: "20px",
  width: "70px",
  height: "34px",
  marginRight: "20px",
  marginLeft: "20px",
  backgroundColor: "white",
  color: "#369",
  fontWeight: "bold",
};


const MainPage = (props) => {
  const [quizzes, setQuizzes] = useState([]);
  const history = useHistory();

  useEffect(() => {
    if (window.localStorage.getItem("isAuth") === null) {
      window.localStorage.setItem("isAuth", "false");
    }
    if (window.localStorage.getItem("isAuth") === "true") getQuiz();
   
  }, []);

  const getQuiz = async () => {
    try{
      const response = await axios.get(`${USER_SERVER}/api/showquiz`);
      console.log(response);
      if (response.data.success) {
        setQuizzes(response.data.quiz_list);
      }
    }catch(error) {
      //if(error.response.status===401){
      //  alert(error.response.data.message);
      //  window.localStorage.setItem("isAuth", "false");
      //}
    }
  };

  //const history = useHistory();
  const [fileUrl, setFileUrl] = useState(null);
  const [fileImg, setFileImg] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [resultVal, setValue] = useState('');
  const [resultName, setName] = useState('');
  const [resultJson, setJson] = useState({
    quiz_id: "",
    title: "",
    answer: "",
    script: "",
    image: "",
    score: "",
  });

  const stateUpdate = (imageUrl, imageFile) => {
    setFileUrl(imageUrl);
    setFileImg(imageFile);
  };

  // 이미지 업로드 버튼 이벤트. 미리보기
  async function processImage(event) {
    const imageFile = event.target.files[0];
    const imageUrl = URL.createObjectURL(imageFile);
    await stateUpdate(imageUrl, imageFile);
  }

  // 모달 여는 함수
  const openModal = () => {
    if (window.localStorage.getItem("isAuth") === "true") {
      setModalOpen(true);
      setFileUrl(null);
    } else {
      alert("로그인을 먼저 해주세요!");
      setModalOpen(false);
    }
  };

  // 모달 닫는 함수
  const closeModal = () => {
    setModalOpen(false);
  };

  // 확정 버튼 onClick 함수
  const decideData = () => {
    if (window.localStorage.getItem("isAuth") === "true") {
      alert("확정버튼 누름");
    } else {
      alert("로그인 먼저 해주세요!");
    }
  };

  // 수정 버튼 onClick 함수
  const changeData = () => {
    if (window.localStorage.getItem("isAuth") === "true") {
      alert("수정버튼 누름");
    } else {
      alert("로그인 먼저 해주세요!");
    }
  };
  
  /*
  const changeText = (e) => {
    this.setState({
      [e.target.name] : e.target.value,
    });
    alert(e.target.value);
  };
  */
  
  
  // 바뀌는 value값 저장
  const handleSave = ({value}) => {
    setValue(value);

    console.log("value:" + value);
    console.log("setValue:" + resultVal);
    //alert(name);
    //console.log(e.tableProps);
    //alert(value);
    //alert(name);
    //alert(className);
    //console.log(className);
    //alert(resultJson.title);
  }

  // 바뀌는 값의 json 저장 -> 이값은 나중에 확정 버튼 누르면 서버로 가게.
  const changeQuiz = async(quiz) => {

    let q_choices = [];
    q_choices.push(quiz.choice1, quiz.choice2, quiz.choice3, quiz.choice4, quiz.choice5);
    const changedquiz = {
      _id: quiz._id,
      title: quiz.title,
      answer: Number(quiz.answer),
      script: quiz.script,
      image: quiz.image,
     // score: quiz.score,
      choices: q_choices,
    };
    
    // quiz.choices.map((choice, i) => {
    //   changedquiz[`choice${i + 1}`] = choice;
    // });
    setJson(changedquiz); // 혹시 몰라서 상태 저장
    setJson({
      ...resultJson,
      [resultName] : resultVal 
    });

    console.log(quiz);
    console.log(resultVal);
    try {
      const request = await axios
        .post(`${USER_SERVER}/api/quizmodify`, { data: resultJson })
        .then((response) => window.location.replace("/"));
    } catch {
      console.log("error");
    }
  };

  const test = async(quiz, name, value) => {
    console.log(quiz);
    console.log(name);
    console.log(value);
  }

  const test2 = ({value}) => {
    alert(value);
    setValue(value);
    //setName(value);
    //alert(resultName);
    alert(resultVal);
  }

  
  //input data
  const columns = useMemo(
    () => [
      {
        accessor: "qid",
        Header: "문항번호",
        Cell: (tableProps) => (
          <EditText  onSave={(e) => handleSave} onChange={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        )
      },
      {
        accessor: "title",
        Header: "문항내용",
        Cell: (tableProps) => (
          <EditText name="title" onChange={handleSave} onSave={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: "script",
        Header: "참고내용",
        Cell: (tableProps) => (
          <EditText  onSave={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: `choice1`,
        Header: "선택01",
        Cell: (tableProps) => (
          <EditText  onSave={() => test(tableProps.row.original,"choice1", tableProps.cell.value)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: "choice2",
        Header: "선택02",
        Cell: (tableProps) => (
          
          <div>
            <EditText  onChange={setName}  onSave={test2} defaultValue={tableProps.cell.value}/>
            <p>{resultName}</p>
          </div>
        ),  
      },
      {
        accessor: "choice3",
        Header: "선택03",
        Cell: (tableProps) => (
          <EditText  onSave={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: "choice4",
        Header: "선택04",
        Cell: (tableProps) => (
          <EditText  onSave={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: "choice5",
        Header: "선택05",
        Cell: (tableProps) => (
          <EditText  onSave={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: "answer",
        Header: "정답",
        Cell: (tableProps) => (
          <EditText  onSave={() => changeQuiz(tableProps.row.original)}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        accessor: "score",
        Header: "점수",
        Cell: (tableProps) => (
          <EditText  onSave={handleSave}  defaultValue={tableProps.cell.value}/>
        ),  
      },
      {
        Header: "Delete",
        id: "delete",
        accessor: (str) => "delete",

        Cell: (tableProps) => {
          return (
            <span
              style={{
                cursor: "pointer",
                color: "blue",
                textDecoration: "underline",
              }}
              onClick={() => deleteQuiz(tableProps.row.original._id)}
            >
              Delete
            </span>
          );
        },
      },
    ],
    [quizzes]
  );
  const data = useMemo(() => {
    const showed_data = quizzes?.map((quiz) => {
      let data_return = {
        _id: quiz._id,
        qid: "0001",
        title: quiz.title,
        answer: quiz.answer,
        script: quiz.script,
        image: quiz.image,
        score: "3점",
      };

      quiz.choices.map((choice, i) => {
        data_return[`choice${i + 1}`] = choice;
      });

      return data_return;
    });
    return showed_data;
  }, [quizzes]);

  // 전송 버튼 클릭 이벤트
  const sendImage = () => {
    const formData = new FormData();
    formData.append("image", fileImg);
    console.log(formData);
    if(fileImg===null){ //이미지 선택 안하고 업로드 버튼 눌렀을 때 버그 수정
      alert("이미지가 선택되지 않았습니다");
    }
    else{
      try {
        const request = axios
          .post(`${USER_SERVER}/api/imageupload`, formData, {
            withCredentials: true,
          })
          .then(function (response) {
            if (response.data.success) {  //성공적으로 이미지 업로드 시 replace
              console.log(response);
              window.location.replace("/");
            } 
          });
      }catch(error) {
        alert(error.response.data.message);
      }
    }
    closeModal();
  };

  // 삭제 버튼 클릭 이벤트
  const deleteQuiz = async (quiz_id) => {
    const deletedquiz = { quiz_id: quiz_id };
    try {
      const request = await axios
        .delete(`${USER_SERVER}/api/quizdelete`, { data: deletedquiz })
        .then((response) => window.location.replace("/"));
    } catch {
      console.log("error");
    }
  };

  //<BlankTop DesktopMargin='100' TabletMargin='3' MobileMargin='1'/>
  return (
    <div
      style={{
        backgroundColor: "#f0f8ff",
        width: "100vw",
        height: "88vh",
        marginTop: "80px",
      }}
    >
      <div className="nav">
        <Header />
      </div>
      {window.localStorage.getItem("isAuth") === "true" ? (
        <div>
          <div className="content">
            <img
              src={addImg}
              alt="imgadd"
              onClick={openModal}
              style={{
                width: "100px",
                height: "100px",
                cursor: "pointer",
                marginLeft: "25px",
                padding: "0",
                float: "left",
              }}
            />
            <Modal open={modalOpen} close={closeModal}>
              <div style={divBorder}>
                <img
                  style={{
                    objectFit: "fill",
                    width: "150px",
                    height: "200px",
                    border: "solid 1px black",
                  }}
                  src={fileUrl}
                  alt={fileUrl}
                />
              </div>
              <div>
                <input
                  type="file"
                  accept="image/*"
                  name="question_img"
                  onChange={processImage}
                ></input>
                <button onClick={sendImage}>전송</button>
              </div>
            </Modal>
          </div>
          <div
            className="table"
            align="center"
            style={{
              marginRight: "auto",
              width: "85vw",
              height: "70vh",
              overflow: "auto",
              border: "solid 2px black",
              marginLeft: "auto",
              float: "left",
              marginTop: "30px",
            }}
          >
            <Table columns={columns} data={data} />
          </div>
          <div
            className="confirm"
            style={{ clear: "both", textAlign: "center" }}
          >
            <button style={btn} onClick={decideData}>
              확정
            </button>
            <button style={btn} onClick={changeData}>
              수정
            </button>
          </div>
          <footer
            style={{
              backgroundColor: "black",
              color: "white",
              height: "3vh",
              width: "100%",
              position: "fixed",
              bottom: "0",
            }}
          >
            <div>
              아이콘 제작자:{" "}
              <a
                style={{ textDecoration: "none", color: "white" }}
                href="https://www.flaticon.com/kr/authors/pixel-perfect"
                title="Pixel perfect"
              >
                Pixel perfect
              </a>{" "}
              from{" "}
              <a
                style={{ textDecoration: "none", color: "white" }}
                href="https://www.flaticon.com/kr/"
                title="Flaticon"
              >
                www.flaticon.com
              </a>
            </div>
          </footer>
        </div>
      ) : (
        <div>
          <p>로그인이 필요합니다.</p>
        </div>
      )}
    </div>
  );
};

export default MainPage;
