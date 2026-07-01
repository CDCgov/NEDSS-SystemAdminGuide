const KRAMDOWN_ATTR_ROW = /^\{:\s*[^}]+\}$/;

function getRowCellTexts(tokens, rowOpenIndex, rowCloseIndex) {
  const cellTexts = [];
  let currentCellText = null;

  for (let index = rowOpenIndex + 1; index < rowCloseIndex; index += 1) {
    const token = tokens[index];

    if (token.type === 'td_open' || token.type === 'th_open') {
      currentCellText = [];
    } else if (token.type === 'td_close' || token.type === 'th_close') {
      if (currentCellText) {
        cellTexts.push(currentCellText.join('').trim());
        currentCellText = null;
      }
    } else if (currentCellText && token.type === 'inline') {
      currentCellText.push(token.content);
    }
  }

  return cellTexts;
}

module.exports = function kramdownTableAttrFilter(md) {
  md.core.ruler.after('block', 'kramdown_table_attr_filter', (state) => {
    const { tokens } = state;

    for (let tableCloseIndex = tokens.length - 1; tableCloseIndex >= 0; tableCloseIndex -= 1) {
      if (tokens[tableCloseIndex].type !== 'table_close') {
        continue;
      }

      let tableOpenIndex = -1;
      for (let index = tableCloseIndex - 1; index >= 0; index -= 1) {
        if (tokens[index].type === 'table_open') {
          tableOpenIndex = index;
          break;
        }
      }

      if (tableOpenIndex < 0) {
        continue;
      }

      let tbodyOpenIndex = -1;
      let tbodyCloseIndex = -1;
      for (let index = tableOpenIndex + 1; index < tableCloseIndex; index += 1) {
        if (tokens[index].type === 'tbody_open') {
          tbodyOpenIndex = index;
        } else if (tokens[index].type === 'tbody_close') {
          tbodyCloseIndex = index;
          break;
        }
      }

      if (tbodyOpenIndex < 0 || tbodyCloseIndex < 0) {
        continue;
      }

      let rowCloseIndex = -1;
      for (let index = tbodyCloseIndex - 1; index > tbodyOpenIndex; index -= 1) {
        if (tokens[index].type === 'tr_close') {
          rowCloseIndex = index;
          break;
        }
      }

      if (rowCloseIndex < 0) {
        continue;
      }

      let rowOpenIndex = -1;
      for (let index = rowCloseIndex - 1; index > tbodyOpenIndex; index -= 1) {
        if (tokens[index].type === 'tr_open') {
          rowOpenIndex = index;
          break;
        }
      }

      if (rowOpenIndex < 0) {
        continue;
      }

      const cellTexts = getRowCellTexts(tokens, rowOpenIndex, rowCloseIndex);
      if (cellTexts.length < 2) {
        continue;
      }

      if (!KRAMDOWN_ATTR_ROW.test(cellTexts[0])) {
        continue;
      }

      if (cellTexts.slice(1).some((text) => text !== '')) {
        continue;
      }

      const attrRowStartLine = tokens[rowOpenIndex].map?.[0];
      if (typeof attrRowStartLine === 'number') {
        if (tokens[tableOpenIndex].map) {
          tokens[tableOpenIndex].map[1] = attrRowStartLine;
        }
        if (tokens[tbodyOpenIndex].map) {
          tokens[tbodyOpenIndex].map[1] = attrRowStartLine;
        }
      }

      tokens.splice(rowOpenIndex, rowCloseIndex - rowOpenIndex + 1);
    }
  });
};