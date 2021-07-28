import React, { useMemo } from "react";
import Header from "../components/Header";
import Table from "../components/Table";
import { useState, useEffect } from "react";
import Loader from "./Loader";
import axios from "axios";
import { USER_SERVER } from "../config";
import Modal from "../components/Modals/Modal.js";
import addImg from "./imgIcon.png";
import noLoginImg from "./noLogin.PNG";
import { useHistory } from "react-router-dom";
import { EditText } from "react-edit-text";
import TableCell from "../components/TableCell";

// 테두리 만드는 css
const divBorder = {
  marginBottom: "40px",
  position: "relation",
};

// hover 관련 image css
const imgStyle = {
  width: "300px",
  marginRight: "10px",
  display: "block",
  backgroundColor: "white",
};

// hover 관련 div css
const divHover = {
  position: "absolute",
  alignItems: "center",
  justifyContent: "center",
  //left: "25%",
  //top: "12%",
  backgroundColor: "#f2f2f2",
  borderRadius: "10px",
  paddingTop: "0px",
  marginTop: "35px",
};

const MainPage = (props) => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [HoveredRow, setHoveredRow] = useState();
  const [HoveredColumn, setHoveredColumn] = useState();
  const [toggle, setToggle] = useState(true);

  useEffect(() => {
    if (window.localStorage.getItem("isAuth") === null) {
      window.localStorage.setItem("isAuth", "false");
    }
    if (window.localStorage.getItem("isAuth") === "true") getQuiz();
  }, [isHovered, toggle]);

  const getQuiz = async () => {
    try {
      const response = await axios.get(`${USER_SERVER}/api/v1/quiz/show`);
      console.log(response);
      if (response.data.success) {
        setQuizzes(response.data.quiz_list);
      }
    } catch (error) {
      // if (error.response.status === 401) {
      //   alert(error.response.data.message);
      //   window.localStorage.setItem("isAuth", "false");
      //   setToggle(!toggle);
      // }
    }
  };

  const [fileUrl, setFileUrl] = useState(null);
  const [fileImg, setFileImg] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

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

  // 바뀌는 value값 저장
  const handleSave = async (quiz, e) => {
    console.log(e.name);
    const tmp = e.name.split(",");
    const name = tmp[0];
    let idx = 0;
    if (tmp.length === 2) idx = tmp[1];
    const changedValue = await changeQuiz(name, idx, e.value, quiz);
    console.log(changedValue);
    try {
      const request = await axios
        .put(`${USER_SERVER}/api/v1/quiz/modify`, changedValue)
        .then(() => {
          alert("수정되었습니다.");
          window.location.replace("/");
        });
    } catch {
      console.log("error");
    }
  };

  const changeQuiz = async (name, idx, value, quiz) => {
    console.log(name);
    let arr = quiz[`${name}`];
    let tmp_arr = [];
    if (typeof arr === "object") {
      arr.map((content, i) => {
        if (Number(idx) === i) {
          tmp_arr.push(value);
        } else {
          tmp_arr.push(content);
        }
      });
      quiz = { ...quiz, [name]: tmp_arr };
    } else {
      quiz = { ...quiz, [name]: value };
    }
    const quiz_to_return = {
      _id: quiz._id,
      title: quiz.title,
      choices: [],
      answer: quiz.answer,
      script: quiz.script,
      image: quiz.image,
      score: quiz.score,
    };
    let tmp_arr2 = [];
    [1, 2, 3, 4, 5].map((num) =>
      quiz[`choice${num}`]?.map((choice) => tmp_arr2.push(choice))
    );
    quiz_to_return.choices = tmp_arr2;
    return quiz_to_return;
  };

  const getUrls = (urls) => {
    const url_arr = [];
    if (typeof urls === "object") {
      urls.map((url, i) => {
        if (url.substring(0, 25) === "https://summer-program.s3") {
          url_arr.push(url);
        }
      });
    } else if (urls.substring(0, 25) === "https://summer-program.s3") {
      url_arr.push(urls);
    }
    if (url_arr.length !== 0) {
      return url_arr;
    }
  };

  const setTarget = (row, column) => {
    setHoveredColumn(column);
    setHoveredRow(row);
    setIsHovered(true);
  };

  //테이블에 들어가는 내용(columns, data)
  const columns = useMemo(
    () => [
      {
        accessor: "title",
        Header: "질문",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="title"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "script",
        Header: "보기",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="script"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "choice1",
        Header: "선택01",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="choice1"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "choice2",
        Header: "선택02",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="choice2"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "choice3",
        Header: "선택03",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="choice3"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "choice4",
        Header: "선택04",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="choice4"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "choice5",
        Header: "선택05",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="choice5"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "answer",
        Header: "정답",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="answer"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        accessor: "score",
        Header: "점수",
        Cell: (tableProps) => {
          const urls = getUrls(tableProps.cell.value);
          return (
            <TableCell
              title="score"
              isHovered={isHovered}
              HoveredRow={HoveredRow}
              HoveredColumn={HoveredColumn}
              setIsHovered={setIsHovered}
              setTarget={setTarget}
              tableProps={tableProps}
              urls={urls}
              handleSave={handleSave}
            />
          );
        },
      },
      {
        Header: "삭제 ",
        id: "delete",
        accessor: (str) => "delete",

        Cell: (tableProps) => {
          return (
            <span
              style={{
                display: "inline-block",
                width: "40px",
                cursor: "pointer",
                color: "#FD745D",
                textDecoration: "underline",
              }}
              onClick={() => {
                if (window.confirm("정말 삭제하시겠습니까?") === true) {
                  //확인
                  deleteQuiz(tableProps.row.original._id);
                } else {
                  //취소
                  return false;
                }
              }}
            >
              삭제
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
        title: quiz.title,
        answer: quiz.answer,
        script: quiz.script,
        image: quiz.image,
        score: quiz.score,
        choice1: [],
        choice2: [],
        choice3: [],
        choice4: [],
        choice5: [],
        choice6: [],
        choice7: [],
        choice8: [],
        choice9: [],
      };
      let url_idx = 1;
      let txt_idx = 1;
      quiz.choices.map((choice, i) => {
        if (
          choice.substring(0, 25) === "https://summer-program.s3" ||
          choice === "no exist url"
        ) {
          data_return[`choice${url_idx++}`].push(choice);
        } else {
          data_return[`choice${txt_idx++}`].push(choice);
        }
      });

      return data_return;
    });
    return showed_data;
  }, [quizzes]);

  // 전송 버튼 클릭 이벤트
  const sendImage = () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("image", fileImg);
    console.log(formData);
    if (fileImg === null) {
      //이미지 선택 안하고 업로드 버튼 눌렀을 때 버그 수정
      alert("이미지가 선택되지 않았습니다");
    } else {
      try {
        const request = axios
          .post(`${USER_SERVER}/api/v1/quiz/imageupload`, formData, {
            withCredentials: true,
          })
          .then(function (response) {
            if (response.data.success) {
              setLoading(false);
              //성공적으로 이미지 업로드 시 replace
              console.log(response);
              window.location.replace("/");
              alert("문제가 등록되었습니다.");
            }
          });
      } catch (error) {
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
        .delete(`${USER_SERVER}/api/v1/quiz/delete`, { data: deletedquiz })
        .then((response) => window.location.replace("/"));
      alert("문제가 삭제되었습니다.");
    } catch {
      console.log("error");
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#f5f6f7",
        width: "100vw",
        minHeight: "88vh",
        marginTop: "80px",
        zIndex: "0",
      }}
    >
      <div className="nav">
        <Header />
      </div>
      {window.localStorage.getItem("isAuth") === "true" ? (
        loading ? (
          <Loader type="spin" color="#F7A29B" message={"문제 등록 중입니다."} />
        ) : (
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
                      backgroundColor: "#f2f2f2",
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
                  <button
                    style={{ border: "solid 1px black" }}
                    onClick={sendImage}
                  >
                    전송
                  </button>
                </div>
              </Modal>
            </div>
            <div
              className="table"
              align="center"
              style={{
                marginRight: "auto",
                width: "85vw",
                maxHeight: "70vh",
                overflow: "auto",
                border: "solid 2px black",
                marginLeft: "auto",
                float: "left",
                marginTop: "60px",
                position: "auto",
                //backgroundColor: 'white',
              }}
            >
              <Table columns={columns} data={data} />
            </div>
            <div
              className="confirm"
              style={{ clear: "both", textAlign: "center" }}
            ></div>
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
        )
      ) : (
        <div>
          <img
            src={noLoginImg}
            alt="noLogin state"
            onClick={() => {
              alert("로그인을 해주세요");
            }}
            style={{
              width: "93vw",
              marginLeft: "auto",
              marginRight: "auto",
              paddingLeft: "30px",
              marginTop: "30px",
            }}
          />
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
      )}
    </div>
  );
};

export default MainPage;
