import React, { useRef, useEffect } from "react";
import { EditText } from "react-edit-text";
import styled from "styled-components";

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
const DivHover = styled.div`
  position: absolute;
  top: ${(props) => props.top || 0}px;
  left: ${(props) => props.left || 0}px;
  align-items: center;
  justify-content: center;
  //left: 25%;
  //top: 12%;
  background-color: #f2f2f2;
  border-radius: 10px;
`;

const TableCell = ({
  title,
  isHovered,
  HoveredRow,
  HoveredColumn,
  setIsHovered,
  setTarget,
  tableProps,
  urls,
  handleSave,
}) => {
  return (
    <div
      title={title}
      onMouseOver={() =>
        document.activeElement.type === "text"
          ? console.log(document.activeElement.type)
          : setTarget(tableProps.cell.row.index, tableProps.cell.column.Header)
      }
      onMouseLeave={() =>
        document.activeElement.type === "text" ? {} : setIsHovered(false)
      }
      style={{
        cursor: "pointer",
        width: "90%",
        height: "90%",
        textAlign: "center",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      {isHovered &
        (HoveredRow === tableProps.cell.row.index) &
        (HoveredColumn === tableProps.cell.column.Header) &
        (typeof urls === "object") && urls.length !== 0 ? (
        <DivHover>
          <header
            style={{
              backgroundColor: "#f2f2f2",
              position: "relative",
              borderRadius: "10px",
            }}
          >
            <h3>이미지 미리보기</h3>
          </header>
          <main style={{ backgroundColor: "white", marginTop: "10px" }}>
            {urls?.map((url, i) => (
              <img alt="이미지" src={url} style={imgStyle} />
            ))}
          </main>
        </DivHover>
      ) : (
        <></>
      )}
      {typeof tableProps.cell.value === "object" ? (
        tableProps.cell.value.map((content, i) => {
          if (
            content.substring(0, 25) === "https://summer-program.s3" ||
            content === "no exist url"
          ) {
            return <div></div>; //<EditText readonly="true" defaultValue="img_url" />;
          } else {
            return (
              <EditText
                name={`${title},${i}`}
                onSave={(e) => handleSave(tableProps.row.original, e)}
                defaultValue={content}
              />
            );
          }
        })
      ) : tableProps.cell.value.substring(0, 25) ===
        "https://summer-program.s3" ? (
        <></> //<EditText readonly="true" defaultValue="img_url" />;
      ) : (
        <EditText
          name={`${title}`}
          onSave={(e) => handleSave(tableProps.row.original, e)}
          defaultValue={tableProps.cell.value}
        />
      )}
    </div>
  );
};

export default TableCell;
