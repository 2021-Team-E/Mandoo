<div align="center">
  <h1>
    React Table CSS Unit
    <br/>
    <br/>
  </h1>
  <br/>
  <br/>
  <a href="https://www.npmjs.com/package/react-table-css-unit">
    <img src="https://img.shields.io/npm/v/react-table-css-unit.svg" alt="npm package" />
  </a>
  <br/>
  <br/>
  Make the <code>column.width</code> of <a href="https://github.com/tannerlinsley/react-table">React Table v7</a> support various css units, such as '200px', '200%', '200vh', etc.
  <br/>
  <br/>
  <pre>npm i <a href="https://www.npmjs.com/package/react-table-css-unit">react-table-css-unit</a></pre>
  <br/>
</div>

__*Tips:* It will cause plugins and features
that depend on the value caculation of `column.wide` invalid, such as `useResizeColumns`, etc.__

## Documentation
* [Simple example](#simple-example)
* [Full example](#full-example)
* [Contribute](#contribute)

## Simple example
```js
const columns = [
  {
    Header: 'Name',
    accessor: 'name',
    width: '100px',
  },
  {
    Header: 'Age',
    accessor: 'age',
    width: '80%'
  }
]
```

## Full example

```js
import React, { useMemo } from 'react'
import ReactDom from 'react-dom'
import { useTable, useBlockLayout } from 'react-table'
import styled from 'styled-components'

import { useCssUnit } from 'react-table-css-unit'

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

function Table() {
  const data = useMemo(() => [...], [])
  const columns = useMemo(() => 
    [{
      Header: '100px',
      accessor: 'col0'
    }, {
      Header: '20%',
      accessor: 'col1'
    }, {
      Header: '20vw',
      accessor: 'col2'
    }, {
      Header: '30vh',
      accessor: 'col3'
    }, {
      Header: '100', // 100px
      accessor: 'col4'
    }, {
      Header: '20em',
      accessor: 'col5'
    }, {
      Header: '20rem',
      accessor: 'col6'
    }].map(c => ({
      ...c,
      width: c.Header
    }))
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
  <Table />,
  document.querySelectof('#app')
)
```

## Contribute

* `git clone https://github.com/jsonz1993/react-table-css-unit.git`
* `npm install`
* `npm run demo`
* Go to http://localhost:9999
