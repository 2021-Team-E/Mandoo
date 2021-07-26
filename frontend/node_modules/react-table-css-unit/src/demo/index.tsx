import React, { useMemo } from 'react'
import ReactDom from 'react-dom'
import { useTable, useBlockLayout } from 'react-table'
import styled from 'styled-components'

import { generateData } from './util'
import { useCssUnit } from '../index'

const Styles = styled.div`
  padding: 1rem;

  .table {
    border: 1px solid #ddd;

    .theader,
    .tbody {
      width: fit-content;
    }

    .th,
    .td {
      padding: 5px;
      border-bottom: 1px solid #ddd;
      border-right: 1px solid #ddd;
      background-color: #fff;
      overflow: hidden;
    }
  }
`


function Demo() {
  const data = useMemo(() => generateData(10, 10), [])
  const columns = useMemo(() =>
     [{
      Header: '100', // 100px
      accessor: 'col0',
      width: '100'
    }, {
      Header: 'parent',
      columns: [
        {
          Header: '10rem',
          width: '10rem',
          accessor: 'col1'
        },
        {
          Header: '100px',
          width: '100px',
          accessor: 'col2'
        }
      ]
    }, {
      Header: '30vh',
      width: '30vh',
      accessor: 'col3'
    }, {
      Header: '100px',
      width: '100px',
      accessor: 'col4'
    }, {
      Header: '20em',
      width: '20em',
      accessor: 'col5'
    }, {
      Header: '20rem',
      width: '20rem',
      accessor: 'col6'
    }]
  , [])

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      data,
      columns,
    },
    useBlockLayout,
    useCssUnit,
  )


  return (
    <div {...getTableProps()} className="table">
      <div className="theader">
      {
        headerGroups.map(headerGroup => (
          <div
            {...headerGroup.getHeaderGroupProps()}
            className="tr"
          >
              {
                headerGroup.headers.map(column => {
                  return (
                    <div {...column.getHeaderProps()} className="th">
                      {column.render('Header')}
                    </div>
                  )
                })
              }

          </div>
        ))
      }
      </div>
      <div {...getTableBodyProps()} className="tbody">
        {
          rows.map(row => {
            prepareRow(row)
            return (
              <div {...row.getRowProps()} className="tr">
                {
                  row.cells.map(cell => {
                    return (
                      <div {...cell.getCellProps()} className="td">
                        {cell.render('Cell')}
                      </div>
                    )
                  })
                }
              </div>
            )
          })
        }
      </div>
    </div>
  )
}

ReactDom.render(
  <Styles>
    <Demo />
  </Styles>,
  document.querySelector('#app'),
)
