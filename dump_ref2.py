import docx, sys
from docx.table import Table
from docx.text.paragraph import Paragraph
d = docx.Document('reference_format.docx')
o = open('ref_dump2.txt', 'w', encoding='utf-8')
for sn in ['Normal', 'Body Text', 'List Paragraph', 'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5']:
    s = d.styles[sn]
    o.write(f"STYLE {sn}: font={s.font.name} size={s.font.size.pt if s.font.size else None} bold={s.font.bold} align={s.paragraph_format.alignment}\n")
rpr = d.styles.element.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPrDefault')
o.write('DEFAULT RPR: ' + (__import__('lxml.etree').etree.tostring(rpr).decode()[:600] if rpr is not None else 'none') + '\n')
els = list(d.element.body.iterchildren())
def tdump(idx, maxrows=200):
    t = Table(els[idx], d)
    o.write(f"\n=== TABLE at {idx} style={t.style.name if t.style else None}\n")
    for r in t.rows[:maxrows]:
        o.write(' || '.join(c.text.replace('\n', ' / ')[:70] for c in r.cells) + '\n')
for idx in [0, 35, 49, 65, 69, 108, 128, 132, 136, 138, 496]:
    tdump(idx)
for idx in range(55, 140):
    el = els[idx]
    if el.tag.endswith('}p'):
        p = Paragraph(el, d)
        if p.text.strip():
            o.write(f"P{idx}: {p.text}\n")
# section footers xml
for i, s in enumerate(d.sections):
    o.write(f"\nSECTION {i} footer xml:\n{s.footer._element.xml[:1500]}\n")
    pg = s._sectPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType')
    o.write('pgNumType: ' + (__import__('lxml.etree').etree.tostring(pg).decode() if pg is not None else 'None') + '\n')
o.write('\nRAW XML cover title table:\n' + els[0].xml[:3000])
o.write('\nRAW XML table 496 first rows:\n' + els[496].xml[:5000])
o.write('\nRAW XML chapter heading 140 + body 142 + section 145:\n' + els[139].xml + els[140].xml + els[142].xml[:2500] + els[145].xml[:2000])
o.write('\nRAW caption 495:\n' + els[495].xml[:2000])
o.write('\nRAW img para 335 & caption 336:\n' + els[335].xml[:3000] + els[336].xml[:1500])
o.write('\nRAW references heading 699 + 700:\n' + els[699].xml[:2000] + els[700].xml[:2000])
for k in range(156, 166):
    o.write(f'\nRAW {k}:\n' + els[k].xml[:800])
o.close()
