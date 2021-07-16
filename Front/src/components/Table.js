import React from 'react';
import { useTable, useGlobalFilter, useSortBy } from 'react-table';
import Search from './Search';

function Table({ columns, data }) {
  const {
    getTableProps, //<Table>에 적용할 prop
    getTableBodyProps, // <tbody>에 적용할 prop
    headerGroups, // <thead> 에서 렌더링할 데이터
    rows, // <tbody>에서 랜더링할 데이터
    prepareRow,
    setGlobalFilter,
  } = useTable({ columns, data }, useGlobalFilter, useSortBy);

  return (
    <>
      <div style={{ top: '0', position: 'sticky', backgroundColor: '#369' }}>
        <Search onSubmit={setGlobalFilter} />
      </div>

      <table
        {...getTableProps()}
        border="1"
        align="center"
        style={{
          backgroundColor: 'white',
          borderCollapse: 'collapse',
          width: '100%',
        }}
      >
        <thead
          style={{
            borderBottom: '2px solid #036',
            color: 'white',
            top: '24px',
            position: 'sticky',
            backgroundColor: '#369',
          }}
        >
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render('Header')}
                </th>
              ))}
            </tr>
          ))}
        </thead>

        <tbody {...getTableBodyProps()} align="center">
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}

export default Table;
