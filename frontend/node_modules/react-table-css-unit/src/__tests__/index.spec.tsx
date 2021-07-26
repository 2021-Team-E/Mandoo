import { useBlockLayout, useTable } from 'react-table'
import React from 'react'
import { generateData } from '../demo/util'
import { getRealStyle, useCssUnit } from '../index'
import { render } from '@testing-library/react'

function App({
  options= {data, columns},
  plugins= [useBlockLayout, useCssUnit],
  useTableRef
}: any): any {

  const instance = useTable(options, ...plugins)

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = instance

  if (useTableRef) {
    useTableRef.current = instance
  }

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

const data = generateData(1, 10)
const columns = [{
  Header: 'col0',
  accessor: 'col0',
  width: '20%'
}, {
  Header: 'col1',
  accessor: 'col1',
  width: '200'
}]


function getWidth(widthWithCssUnit: any, style: any = {}): string{
  return getRealStyle(style, {
    widthWithCssUnit
  }).width
}

describe('use-css-unit-tests', () => {
  it('getRealStyle: style is undefined', () => expect(getWidth('100px')).toEqual('100px'))

  //
  it('getRealStyle: column.width = 100', () => expect(getWidth(100)).toEqual(100))

  it('getRealStyle: column.width(px)', () => expect(getWidth('100px')).toEqual('100px'))

  it('getRealStyle: column.width(vw)', () => expect(getWidth('100vh')).toEqual('100vh'))

  interface tableInstanceInterface {
    current: any
  }

  it('useCssUnit tableInstance.flatHeaders.props', () => {
    const tableInstance: tableInstanceInterface = { current: null }
    render(<App useTableRef={tableInstance} />)
    const flatHeaders = tableInstance.current.flatHeaders
    const widths = flatHeaders.map((header: any) => header.getHeaderProps().style.width)
    return expect(widths).toStrictEqual(['20%', '200px'])
  })

})
