import React from "react";
import { EditText } from "react-edit-text";

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
      onMouseEnter={() =>
        document.activeElement.type === "text"
          ? console.log(document.activeElement.type)
          : setTarget(tableProps.cell.row.index, tableProps.cell.column.Header)
      }
      onMouseLeave={() =>
        document.activeElement.type === "text" ? {} : setIsHovered(false)
      }
      style={{ cursor: "pointer" }}
    >
      {isHovered &
        (HoveredRow === tableProps.cell.row.index) &
        (HoveredColumn === tableProps.cell.column.Header) &
        (typeof urls === "object") && urls.length !== 0 ? (
        <div style={divHover}>
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
        </div>
      ) : (
        <></>
      )}
      {typeof tableProps.cell.value === "object" ? (
        tableProps.cell.value.map((content, i) => {
          if (content.substring(0, 25) === "https://summer-program.s3") {
            return <>img_url</>; //<EditText readonly="true" defaultValue="img_url" />;
          }
          return (
            <EditText
              name={`${title},${i}`}
              onSave={(e) => handleSave(tableProps.row.original, e)}
              defaultValue={content}
            />
          );
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
