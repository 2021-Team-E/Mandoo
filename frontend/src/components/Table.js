import React from "react";
import { useTable, useGlobalFilter } from "react-table";
import Search from "./Search";

function Table({ columns, data }) {
  const {
    getTableProps, //<Table>에 적용할 prop
    getTableBodyProps, // <tbody>에 적용할 prop
    headerGroups, // <thead> 에서 렌더링할 데이터
    rows, // <tbody>에서 랜더링할 데이터
    prepareRow, //렌더링 할 데이터 준비하는 함수
    setGlobalFilter, //<search> 컴포넌트에 prop으로 전달
  } = useTable({ columns, data }, useGlobalFilter); //useGlobalFilter(): 전체 데이터 검색

  return (
    <>
      <div style={{ top: "0", position: "sticky", backgroundColor: "#369" }}>
        <Search onSubmit={setGlobalFilter} />{" "}
        {/*setGolbalFilter 함수 호촐되고 rows 배열에 필터링된 검색 결과 반영 */}
      </div>

      <table
        {...getTableProps()}
        border="1"
        align="center"
        style={{
          backgroundColor: "white",
          borderCollapse: "collapse",
          width: "100%",
        }}
      >
        <thead
          style={{
            borderBottom: "2px solid #036",
            color: "white",
            top: "31.5px",
            position: "sticky",
            backgroundColor: "#369",
          }}
        >
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(
                (
                  column //각 칸에 Header map
                ) => (
                  <th {...column.getHeaderProps()}>
                    {column.render("Header")}
                  </th>
                )
              )}
            </tr>
          ))}
        </thead>

        <tbody
          title="표 안의 내용을 클릭해 수정하세요"
          {...getTableBodyProps()}
          align="center"
        >
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(
                  (
                    cell //각 칸에 data map
                  ) => (
                    <td style={{ height: "40px" }} {...cell.getCellProps()}>
                      {cell.render("Cell")}
                    </td>
                  )
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}

export default Table;
