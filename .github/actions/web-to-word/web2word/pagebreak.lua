-- Turn <div class="page-break"></div> markers (inserted between chapters when
-- merging pages) into real Word page breaks. Pandoc's HTML reader has no native
-- page break, but a Lua filter runs on the AST and can emit raw OOXML.
function Div(el)
  if el.classes:includes("page-break") then
    return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
  end
end
