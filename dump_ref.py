import docx, sys
from docx.text.paragraph import Paragraph
from docx.table import Table
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
d = docx.Document(sys.argv[1] if len(sys.argv) > 1 else 'reference_format.docx')
out = open('ref_dump.txt', 'w', encoding='utf-8')
for i, el in enumerate(d.element.body.iterchildren()):
    tag = el.tag.split('}')[1]
    if tag == 'p':
        p = Paragraph(el, d)
        sect = 'SECT' if el.find('.//' + W + 'sectPr') is not None else ''
        pb = 'PB' if el.xpath('.//w:br[@w:type="page"]') else ''
        img = 'IMG' if el.xpath('.//a:blip') else ''
        sz = [r.font.size.pt for r in p.runs if r.font.size][:1]
        b = [r.bold for r in p.runs][:1]
        pf = p.paragraph_format
        if p.text.strip() or sect or pb or img:
            out.write(f"{i} {p.style.name} {p.alignment} sz={sz} b={b} ls={pf.line_spacing} fi={pf.first_line_indent} {sect} {pb} {img} | {p.text[:100]}\n")
    elif tag == 'tbl':
        t = Table(el, d)
        out.write(f"{i} TABLE {len(t.rows)}x{len(t.columns)} | " + ' / '.join(c.text[:25] for c in t.rows[0].cells) + "\n")
    else:
        out.write(f"{i} {tag}\n")
out.close()
