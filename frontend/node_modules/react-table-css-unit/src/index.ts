import { ensurePluginOrder } from 'react-table'

function hasCssUnit(style: string): boolean {
  return Number.isNaN(Number(style))
}

function getWidth(width: any): string {
  if (hasCssUnit(width)) return width
  else return `${width}px`
}


export function getRealStyle(style: any={}, column: any): any {
  const { width, widthWithCssUnit } = column

  if (hasCssUnit(width) || widthWithCssUnit) {
    style.width = widthWithCssUnit
  }
  style.flex = 'none'
  return style
}

export const useCssUnit = (hooks: any): void => {
  hooks.useInstance.push(useInstance)

  hooks.getHeaderProps.push(function (props: any, { column }: any) {
    const { style } = props
    return [
      props,{
        style: getRealStyle(style, column)
      }
    ]
  })

  hooks.getCellProps.push(function (props: any, { cell: { column } }: any) {
    const { style } = props
    return [
      props,{
        style: getRealStyle(style, column)
      }
    ]
  })

  hooks.getFooterProps.push(function (props: any, { column }: any) {
    const { style } = props
    return [
      props,{
        style: getRealStyle(style, column)
      }
    ]
  })
}
useCssUnit.pluginName = 'useCssUnit'

function useInstance(instance: any): void {
  const {
    plugins,
    totalColumnsMaxWidth,
    totalColumnsMinWidth,
    totalColumnsWidth,
    calculateColumnsMaxWidth,
    calculateColumnsMinWidth,
    calculateColumnsWidth,
    headers,
  } = instance

  ensurePluginOrder(
    plugins,
    ['useBlockLayout',],
    'useCssUnit'
  )

  if (calculateColumnsWidth) {
    instance.totalColumnsWidth = calculateColumnsWidth(instance, totalColumnsWidth)
  }

  if (calculateColumnsMaxWidth) {
    instance.totalColumnsMaxWidth = calculateColumnsWidth(instance, totalColumnsMaxWidth)
  }

  if (calculateColumnsMinWidth) {
    instance.totalColumnsMinWidth = calculateColumnsMaxWidth(instance, totalColumnsMinWidth)
  }

  calcHeaderWidthWithCssUnit(headers)
}

function calcHeaderWidthWithCssUnit(headers: any[]): string[] {
  return headers.map((header: any) => {
    const { headers : subHeaders } = header

    if (subHeaders && subHeaders.length) {
      const widths = calcHeaderWidthWithCssUnit(subHeaders)
      const width = widths.length > 1? `calc(${widths.join(' + ')})`: widths[0]
      header.widthWithCssUnit = width
      return width
    } else {
      const width = getWidth(header.width)
      header.widthWithCssUnit = width
      return width
    }
  })
}
