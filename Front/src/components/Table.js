import React from 'react';
import { useTable } from "react-table";


function Table({columns, data}) {
    const {
        getTableProps,  //<Table>에 적용할 prop
        getTableBodyProps,  // <tbody>에 적용할 prop
        headerGroups, // <thead> 에서 렌더링할 데이터
        rows, // <tbody>에서 랜더링할 데이터
        prepareRow, 
      } = useTable({ columns, data });

    return (
    <table {...getTableProps()} border ="1" align="center" style={{"backgroundColor":"white", "borderCollapse":"collapse", "width":"100%"}}>
        <thead style={{"borderBottom":"2px solid #036", "color":"#369"}}>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th {...column.getHeaderProps()}>{column.render("Header")}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}  align="center">
        {rows.map((row) => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map((cell) => (
                <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
    );
}

export default Table