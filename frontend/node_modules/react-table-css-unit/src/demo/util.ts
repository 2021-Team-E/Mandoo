
export function generateData(row: number, col: number): any[] {
  const data = []
  for (let i = 0; i< row; i++) {
    const r: {[index: string]: any} = {}
    for (let j = 0; j < col; j++) {
      r[`col${j}`] = `${i}-col${j}`
    }
    data.push(r)
  }
  return data
}
