import React from 'react';
import { useTable } from "react-table";


function Table({columns, data}) {
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
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
                <td {...cell.getCellProps()}><input type="text" value={cell.render("Cell")}/></td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
    );
}

export default Table