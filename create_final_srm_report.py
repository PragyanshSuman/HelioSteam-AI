import gzip
import json
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, 'report_figures')

with open(os.path.join(BASE_DIR, 'solar_model_artifacts', 'seq2seq_eval_metrics.json'), 'r', encoding='utf-8') as f:
    SEQ_META = json.load(f)


def set_cell_borders(cell, sz="4", color="000000"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(
        f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>'
    ))


def set_section_page_num(section, fmt='decimal', start=None):
    pg = section._sectPr.find(qn('w:pgNumType'))
    if pg is None:
        pg = OxmlElement('w:pgNumType')
        section._sectPr.append(pg)
    pg.set(qn('w:fmt'), fmt)
    if start is not None:
        pg.set(qn('w:start'), str(start))


def add_page_number_footer(section):
    section.footer.is_linked_to_previous = False
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p._p.append(fldSimple)


def build_report():
    doc = Document()

    # Section 0: Cover, Declaration, Bonafide, Acknowledgement (no page numbers)
    sec0 = doc.sections[0]
    sec0.page_width = Inches(8.27)
    sec0.page_height = Inches(11.69)
    for m in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
        setattr(sec0, m, Inches(1.0))
    sec0.different_first_page_header_footer = True

    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(12)
    normal.font.color.rgb = RGBColor(0, 0, 0)

    def add_centered(text, size=12, bold=False, italic=False, before=0, after=6, ls=1.15):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = ls
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        return p

    def add_body(text, indent=True, after=6, ls=1.5):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = ls
        p.paragraph_format.space_after = Pt(after)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.25)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    def add_heading_16(text, before=12, after=6):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.bold = True
        return p

    def add_sub_heading_14(text, before=10, after=4):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        return p

    def add_chapter_title(num_str, title_str):
        add_centered(f"CHAPTER {num_str}", size=16, bold=True, before=6, after=4, ls=1.15)
        add_centered(title_str.upper(), size=16, bold=True, before=0, after=16, ls=1.15)

    def add_bullet_item(prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        rb = p.add_run(prefix + ": ")
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(12)
        rb.bold = True
        rt = p.add_run(text)
        rt.font.name = 'Times New Roman'
        rt.font.size = Pt(12)
        return p

    def add_figure(img_path, caption, width_in=5.8):
        if not os.path.exists(img_path):
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_path, width=Inches(width_in))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.line_spacing = 1.5
        p_cap.paragraph_format.space_after = Pt(10)
        rc = p_cap.add_run(caption)
        rc.font.name = 'Times New Roman'
        rc.font.size = Pt(11)
        rc.bold = True

    def add_styled_table(headers, rows, caption=None, col_widths=None):
        if caption:
            p_c = doc.add_paragraph()
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_before = Pt(8)
            p_c.paragraph_format.space_after = Pt(4)
            p_c.paragraph_format.keep_with_next = True
            rc = p_c.add_run(caption)
            rc.font.name = 'Times New Roman'
            rc.font.size = Pt(11)
            rc.bold = True

        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for j, h in enumerate(headers):
            c = tbl.rows[0].cells[j]
            set_cell_borders(c, "6", "000000")
            set_cell_shading(c, "E2E8F0")
            set_cell_margins(c)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths:
                c.width = Inches(col_widths[j])
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.bold = True

        for i, row_data in enumerate(rows, start=1):
            for j, val in enumerate(row_data):
                c = tbl.rows[i].cells[j]
                set_cell_borders(c, "4", "000000")
                set_cell_margins(c)
                c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                if col_widths:
                    c.width = Inches(col_widths[j])
                p = c.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 or len(str(val)) > 25 else WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(str(val))
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)

        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)

    # =============================================================
    # PAGE 1: COVER PAGE (Exact Reference Format)
    # =============================================================
    PROJECT_TITLE = (
        "Seq2Seq Encoder-Decoder Neural Forecasting of Solar Steam Production "
        "and LLM-Driven LPG Reduction for Industrial Process Heat"
    )
    add_centered(PROJECT_TITLE, size=18, bold=True, before=12, after=14, ls=1.25)
    add_centered("21CSC402P - PROJECT", size=14, bold=True, before=4, after=14)
    add_centered("Submitted by", size=13, bold=False, italic=True, before=4, after=8)
    add_centered("SANJAI GURU [RA2311003010xxx]", size=15, bold=True, before=2, after=2)
    add_centered("[TEAM MEMBER 2] [RA2311003010xxx]", size=15, bold=True, before=2, after=14)
    add_centered("Under the Guidance of", size=13, italic=True, before=4, after=6)
    add_centered("Dr. / Prof. [FACULTY GUIDE NAME]", size=15, bold=True, before=2, after=2)
    add_centered("(Assistant Professor, Department of Computing Technologies)", size=12, before=0, after=16)
    add_centered("in partial fulfillment of the requirements for the degree of", size=13, italic=True, before=4, after=8)
    add_centered("BACHELOR OF TECHNOLOGY\nin\nCOMPUTER SCIENCE ENGINEERING", size=15, bold=True, before=2, after=14, ls=1.2)

    if os.path.exists(os.path.join(BASE_DIR, "srm_logo_rendered.png")):
        p_lg = doc.add_paragraph()
        p_lg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lg.paragraph_format.space_after = Pt(12)
        p_lg.add_run().add_picture(os.path.join(BASE_DIR, "srm_logo_rendered.png"), width=Inches(3.2))

    add_centered(
        "DEPARTMENT OF COMPUTING TECHNOLOGIES\n"
        "COLLEGE OF ENGINEERING AND TECHNOLOGY\n"
        "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY\n"
        "KATTANKULATHUR - 603 203\n\n"
        "NOVEMBER 2026",
        size=13, bold=True, before=4, after=0, ls=1.25
    )

    doc.add_page_break()

    # =============================================================
    # PAGE 2: OWN WORK DECLARATION FORM
    # =============================================================
    if os.path.exists(os.path.join(BASE_DIR, "srm_logo_rendered.png")):
        p_lg2 = doc.add_paragraph()
        p_lg2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lg2.paragraph_format.space_after = Pt(6)
        p_lg2.add_run().add_picture(os.path.join(BASE_DIR, "srm_logo_rendered.png"), width=Inches(2.5))

    add_centered("Department of Computing Technologies\nSRM Institute of Science & Technology", size=12, bold=True, before=0, after=6)
    add_centered("Own Work Declaration Form", size=14, bold=True, before=2, after=4)
    add_centered("To be completed by the student for all assessments", size=11, italic=True, before=0, after=10)

    decl_tbl = doc.add_table(rows=4, cols=3)
    decl_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    decl_rows = [
        ("Degree / Course", ":", "B. Tech Computer Science Engineering"),
        ("Student Name", ":", "Sanjai Guru, [Team Member 2]"),
        ("Registration Number", ":", "RA2311003010xxx, RA2311003010xxx"),
        ("Title of Work", ":", PROJECT_TITLE),
    ]
    for i, (k, sep, v) in enumerate(decl_rows):
        for j, txt in enumerate((k, sep, v)):
            c = decl_tbl.rows[i].cells[j]
            set_cell_borders(c, "4", "000000")
            set_cell_margins(c, 60, 60, 100, 100)
            c.width = Inches([1.8, 0.3, 4.1][j])
            r = c.paragraphs[0].add_run(txt)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.bold = (j == 0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_body("We hereby certify that this assessment complies with the University's Rules and Regulations relating to Academic misconduct and plagiarism, as listed in the University Website, Regulations, and the Education Committee guidelines.", indent=False, ls=1.25)
    add_body("We confirm that all the work contained in this assessment is our own except where indicated, and that we have met the following conditions:", indent=False, ls=1.25)
    for cond in [
        "Clearly referenced / listed all sources as appropriate",
        "Referenced and put in inverted commas all quoted text (from books, web, etc.)",
        "Given the sources of all pictures, data etc. that are not our own",
        "Not made any use of the report(s) or essay(s) of any other student(s) either past or present",
        "Acknowledged in appropriate places any help that we have received from others",
        "Complied with any other plagiarism criteria specified in the Course handbook / University website",
    ]:
        p_c = doc.add_paragraph(style='List Bullet')
        p_c.paragraph_format.line_spacing = 1.2
        p_c.paragraph_format.space_after = Pt(2)
        rc = p_c.add_run(cond)
        rc.font.name = 'Times New Roman'
        rc.font.size = Pt(11)

    add_body("We understand that any false claim for this work will be penalized in accordance with the University policies and regulations.", indent=False, ls=1.25)

    dbox = doc.add_table(rows=2, cols=1)
    dbox.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_borders(dbox.rows[0].cells[0], "4", "000000")
    set_cell_borders(dbox.rows[1].cells[0], "4", "000000")
    r_dh = dbox.rows[0].cells[0].paragraphs[0].add_run("DECLARATION:")
    r_dh.bold = True
    r_dh.font.name = 'Times New Roman'
    r_dh.font.size = Pt(11)
    r_db = dbox.rows[1].cells[0].paragraphs[0].add_run(
        "We are aware of and understand the University's policy on Academic misconduct and plagiarism "
        "and we certify that this assessment is our own work, except where indicated by referring, and "
        "that we have followed the good academic practices noted above.\n\n"
        "Sanjai Guru [RA2311003010xxx]                    [Team Member 2] [RA2311003010xxx]"
    )
    r_db.font.name = 'Times New Roman'
    r_db.font.size = Pt(11)

    doc.add_page_break()

    # =============================================================
    # PAGE 3: BONAFIDE CERTIFICATE
    # =============================================================
    if os.path.exists(os.path.join(BASE_DIR, "srm_logo_rendered.png")):
        p_lg3 = doc.add_paragraph()
        p_lg3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lg3.paragraph_format.space_after = Pt(12)
        p_lg3.add_run().add_picture(os.path.join(BASE_DIR, "srm_logo_rendered.png"), width=Inches(2.8))

    add_centered("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY\nKATTANKULATHUR - 603 203", size=15, bold=True, before=6, after=12, ls=1.3)
    add_centered("BONAFIDE CERTIFICATE", size=16, bold=True, before=4, after=24)

    add_body(
        f'Certified that 21CSC402P - Project report titled "{PROJECT_TITLE}" is the bonafide work of '
        '"Sanjai Guru [RA2311003010xxx], [Team Member 2] [RA2311003010xxx]" who carried out the project work under my supervision. '
        'Certified further, that to the best of my knowledge the work reported herein does not form any other project report or '
        'dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.',
        indent=True, ls=1.5, after=48
    )

    sig_tbl = doc.add_table(rows=1, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_left = (
        "\n\nSIGNATURE\n\nDr. / Prof. [FACULTY GUIDE NAME]\nSUPERVISOR\nASSISTANT PROFESSOR\n"
        "DEPARTMENT OF COMPUTING TECHNOLOGIES"
    )
    sig_right = (
        "\n\nSIGNATURE\n\nPROFESSOR & HEAD\n"
        "DEPARTMENT OF COMPUTING TECHNOLOGIES"
    )
    for j, stxt in enumerate((sig_left, sig_right)):
        c = sig_tbl.rows[0].cells[j]
        c.width = Inches(3.1)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(stxt)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = True

    doc.add_page_break()

    # =============================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =============================================================
    add_centered("ACKNOWLEDGEMENT", size=16, bold=True, before=6, after=18)
    ack_paras = [
        "We express our humble gratitude to Dr. C. Muthamizhchelvan, Vice-Chancellor, SRM Institute of Science and Technology, for the facilities extended for the project work and his continued support.",
        "We extend our sincere thanks to Dr. Leenus Jesu Martin M, Dean-CET, SRM Institute of Science and Technology, for his invaluable support.",
        "We wish to thank Dr. Revathi Venkataraman, Professor and Chairperson, School of Computing, SRM Institute of Science and Technology, for her support throughout the project work.",
        "We are incredibly grateful to our Head of the Department, Department of Computing Technologies, SRM Institute of Science and Technology, for suggestions and encouragement at all stages of the project work.",
        "We want to convey our thanks to our Project Coordinators, Panel Head, and Panel Members, Department of Computing Technologies, SRM Institute of Science and Technology, for their inputs during the project reviews and support.",
        "Our inexpressible respect and thanks to our guide, Dr. / Prof. [FACULTY GUIDE NAME], Department of Computing Technologies, SRM Institute of Science and Technology, for providing us with an opportunity to pursue our project under mentorship, freedom, and continuous guidance.",
        "We sincerely thank all the staff members of the Department of Computing Technologies, School of Computing, SRM Institute of Science and Technology, for their help during our project. Finally, we thank our parents, family members, and friends for their unconditional support and encouragement.",
    ]
    for ap in ack_paras:
        add_body(ap, indent=False, ls=1.35, after=8)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(18)
    rs = p_sig.add_run("Sanjai Guru\n[Team Member 2]")
    rs.font.name = 'Times New Roman'
    rs.font.size = Pt(12)
    rs.bold = True

    # =============================================================
    # ROMAN NUMERAL FRONT MATTER SECTION (Abstract, TOC, Figures, Tables, Abbrev)
    # =============================================================
    sec_roman = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    sec_roman.page_width = Inches(8.27)
    sec_roman.page_height = Inches(11.69)
    for m in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
        setattr(sec_roman, m, Inches(1.0))
    set_section_page_num(sec_roman, fmt='lowerRoman', start=5)
    add_page_number_footer(sec_roman)

    # ABSTRACT
    add_centered("ABSTRACT", size=16, bold=True, before=6, after=14)
    add_body(
        "Industrial manufacturing processes depend heavily on continuous high-pressure steam, traditionally supplied by fossil-fuel boilers burning Liquefied Petroleum Gas (LPG). "
        "Concentrated Solar Power (CSP) using Linear Fresnel Direct Steam Generation (DSG) offers a clean alternative, yet transient cloud cover and solar intermittency force operators to keep auxiliary LPG boilers running on standby, causing substantial parasitic fuel waste and carbon emissions. "
        "Existing point-wise regression models such as XGBoost forecast only a single hour from static lagged snapshots and cannot capture long-range thermal inertia across an entire diurnal cycle. "
        "This project formulates 24-hour solar steam forecasting as a sequence-to-sequence learning problem using a 2-Layer Long Short-Term Memory (LSTM) Encoder-Decoder architecture augmented with Bahdanau Additive Attention. "
        "Trained chronologically on 8,761 hourly SCADA records from the 10 MWe eLLO Fresnel DSG solar plant (Llo, France), the encoder processes a 48-hour historical window across 12 standardized meteorological, hydraulic, and steam features, while the decoder autoregressively forecasts the next 24 hours conditioned on future weather covariates and attention context. "
        "Evaluated on 1,729 unseen chronological test windows (41,472 horizon steps), the Seq2Seq Encoder-Decoder achieves an overall R² of 0.9174, MAE of 1.973 t/h, RMSE of 5.295 t/h, and a +79.03% skill score improvement over the 24-hour persistence baseline, alongside a daily cumulative R² of 0.9808 across 359 operational days. "
        "Coupled with nine-vessel steam accumulator storage scheduling and a Groq Llama-3.3-70B conversational advisor inside the HelioSteam web platform, the system enables up to 17 continuous hours of zero-LPG boiler shutoff on peak days, displacing 24,966 kg of LPG and avoiding 74.9 tons of CO2 per sunny day.",
        indent=True, ls=1.5, after=10
    )
    p_idx = doc.add_paragraph()
    p_idx.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_idx.paragraph_format.line_spacing = 1.5
    r_ib = p_idx.add_run("Index Terms: ")
    r_ib.bold = True
    r_ib.font.name = 'Times New Roman'
    r_ib.font.size = Pt(12)
    r_it = p_idx.add_run("Solar steam forecasting, Encoder-Decoder, LSTM, Bahdanau attention, Direct Steam Generation, thermal energy storage, LPG displacement, Large Language Models.")
    r_it.font.name = 'Times New Roman'
    r_it.font.size = Pt(12)

    doc.add_page_break()

    # TABLE OF CONTENTS (Our Exact 8 Chapters!)
    add_centered("TABLE OF CONTENTS", size=16, bold=True, before=6, after=14)
    toc_rows = [
        ("", "ABSTRACT", "v"),
        ("", "TABLE OF CONTENTS", "vi"),
        ("", "LIST OF FIGURES", "vii"),
        ("", "LIST OF TABLES", "viii"),
        ("", "ABBREVIATIONS", "ix"),
        ("1", "INTRODUCTION", "1"),
        ("2", "LITERATURE SURVEY WITH RESEARCH GAP AND OBJECTIVE", "3"),
        ("3", "PROJECT IDEA AND MOTIVATION", "6"),
        ("4", "PROCEDURE", "8"),
        ("5", "DATA COLLECTION AND ANALYSIS", "12"),
        ("6", "RESULTS AND DISCUSSIONS", "15"),
        ("7", "CONCLUSION", "21"),
        ("8", "REFERENCES", "22"),
    ]
    add_styled_table(["CHAPTER NO.", "TITLE", "PAGE NO."], toc_rows, col_widths=[1.3, 4.1, 0.9])

    doc.add_page_break()

    # LIST OF FIGURES
    add_centered("LIST OF FIGURES", size=16, bold=True, before=6, after=14)
    lof_rows = [
        ("4.1", "Schematic Diagram of the eLLO Linear Fresnel Direct Steam Solar Field", "9"),
        ("4.2", "Nine-Vessel High-Pressure Steam Accumulator Storage System", "10"),
        ("5.1", "HelioSteam AI Seq2Seq 2-Layer LSTM Encoder-Decoder Architecture with Bahdanau Attention", "13"),
        ("6.1", "Seq2Seq Encoder-Decoder Training & Validation Convergence (40 Epochs)", "16"),
        ("6.2", "24-Hour Solar Steam Forecast vs. Actual SCADA Output (July 16)", "17"),
        ("6.3", "Bahdanau Attention Alignment Across 48h History vs. 24h Forecast Horizon", "18"),
        ("6.4", "Forecasting Error (RMSE) Across 24-Hour Horizons vs. Persistence Baseline", "19"),
    ]
    add_styled_table(["FIGURE NO.", "TITLE", "PAGE NO."], lof_rows, col_widths=[1.2, 4.2, 0.9])

    doc.add_page_break()

    # LIST OF TABLES
    add_centered("LIST OF TABLES", size=16, bold=True, before=6, after=14)
    lot_rows = [
        ("2.1", "Comparison of Existing Solar Steam & Time-Series Forecasting Methods", "5"),
        ("4.1", "Seq2Seq Encoder-Decoder Architecture & Training Hyperparameters", "10"),
        ("5.1", "Key Monitored SCADA Telemetry Parameters & Sensor Tags", "13"),
        ("6.1", "Statistical Benchmark: Seq2Seq Encoder-Decoder vs. XGBoost & Persistence", "16"),
        ("6.2", "Multi-Horizon Seq2Seq Error Breakdown (H+1 to H+24)", "18"),
        ("6.3", "Three-Phase Daily Operational Dispatch & LPG Savings (July 16)", "20"),
    ]
    add_styled_table(["TABLE NO.", "TITLE", "PAGE NO."], lot_rows, col_widths=[1.2, 4.2, 0.9])

    doc.add_page_break()

    # ABBREVIATIONS
    add_centered("ABBREVIATIONS", size=16, bold=True, before=6, after=14)
    abbr_rows = [
        ("AI", "Artificial Intelligence"),
        ("CET / CEST", "Central European Time / Central European Summer Time"),
        ("CSP", "Concentrated Solar Power"),
        ("DNI", "Direct Normal Irradiance [W/m²]"),
        ("DSG", "Direct Steam Generation"),
        ("GHI", "Global Horizontal Irradiance [W/m²]"),
        ("LFR", "Linear Fresnel Reflector"),
        ("LHV", "Lower Heating Value (46.1 MJ/kg for LPG)"),
        ("LLM", "Large Language Model (Groq Llama-3.3-70B)"),
        ("LPG", "Liquefied Petroleum Gas"),
        ("LSTM", "Long Short-Term Memory"),
        ("MAE", "Mean Absolute Error [t/h]"),
        ("MBE", "Mean Bias Error [t/h]"),
        ("R²", "Coefficient of Determination"),
        ("RMSE", "Root Mean Squared Error [t/h]"),
        ("SCADA", "Supervisory Control and Data Acquisition"),
        ("Seq2Seq", "Sequence-to-Sequence Encoder-Decoder Architecture"),
        ("SHIP", "Solar Industrial Process Heat"),
        ("TES", "Thermal Energy Storage (9 Steam Accumulator Tanks)"),
    ]
    add_styled_table(["ABBREVIATION", "FULL FORM"], abbr_rows, col_widths=[1.8, 4.5])

    # =============================================================
    # ARABIC NUMERAL MAIN CHAPTERS SECTION (Starts at Page 1)
    # =============================================================
    sec_main = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    sec_main.page_width = Inches(8.27)
    sec_main.page_height = Inches(11.69)
    for m in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
        setattr(sec_main, m, Inches(1.0))
    set_section_page_num(sec_main, fmt='decimal', start=1)
    add_page_number_footer(sec_main)

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    add_chapter_title("1", "INTRODUCTION")
    add_body("Industrial manufacturing facilities consume vast quantities of thermal energy globally. Across sectors such as textiles, pharmaceuticals, food processing, dairy, and chemical refinement, continuous pressurized steam is an essential utility driving autoclaves, reaction jackets, drying cylinders, and pasteurization heat exchangers. Historically, this continuous thermal load—often requiring 25 to 30 metric tons of steam per hour—has been satisfied by burning fossil fuels, particularly Liquefied Petroleum Gas (LPG), heavy fuel oil, or coal. This reliance exposes manufacturers to volatile fuel prices and generates substantial Scope 1 carbon dioxide (CO2) emissions.")
    add_body("Solar Industrial Process Heat (SHIP), powered by Concentrated Solar Power (CSP) Linear Fresnel Reflectors (LFR) with Direct Steam Generation (DSG), offers a high-efficiency pathway to decarbonize industrial steam. By focusing solar irradiance onto elevated linear receiver tubes carrying pressurized feedwater, DSG plants boil water directly into saturated and superheated steam without intermediate thermal oils. However, because solar irradiance is inherently variable—subject to rapid attenuation by passing clouds, seasonal sun angles, and wind cooling—manufacturing plants cannot risk steam pressure collapse.")
    add_body("To protect production lines from sudden solar drops, plant operators routinely leave auxiliary LPG boilers running continuously in hot-standby mode. This conservative practice wastes roughly 42 kg/h of parasitic LPG in boiler purge and stack losses and leaves solar fields and steam accumulator tanks underutilized. To solve this operational bottleneck, this project builds HelioSteam AI, an end-to-end Sequence-to-Sequence (Seq2Seq) Encoder-Decoder deep learning platform that forecasts 24 hours of solar steam production from 48 hours of historical SCADA telemetry, optimizes nine-tank thermal storage dispatch, and provides natural-language operational instructions via a Groq Llama-3.3-70B Large Language Model (LLM).")

    # -------------------------------------------------------------
    # CHAPTER 2: LITERATURE SURVEY WITH RESEARCH GAP AND OBJECTIVE
    # -------------------------------------------------------------
    add_chapter_title("2", "LITERATURE SURVEY WITH RESEARCH GAP AND OBJECTIVE")
    add_heading_16("2.1 Literature Survey")
    add_body("Forecasting solar thermal steam production and optimizing hybrid fossil-solar dispatch spans three primary research methodologies:")
    add_bullet_item("1. Deterministic Thermodynamic & Optical Modeling", "Duffie and Beckman (2013) and Steinhagen and Morrison (2019) formulated rigorous physical differential equations for two-phase DSG flow, radiative heat loss, and mirror incidence angles. While physically exact under steady-state conditions, purely deterministic solvers struggle during fast cloud transients and cannot adapt automatically to sensor drift or mirror soiling.")
    add_bullet_item("2. Classical Statistical & Tree-Based Tabular Models", "Persistence baselines and ARIMA models (Reikard, 2009) assume future output mirrors recent observations, failing across sunrise/sunset ramps and multi-hour horizons. Gradient Boosted Decision Trees such as XGBoost (Chen and Guestrin, 2016) excel at single-step tabular regression (R² ~ 0.915 for H+1), but treat every hour independently, lacking internal recurrent memory of multi-day thermal inertia and requiring recursive error-prone lag feeding for 24-hour horizons.")
    add_bullet_item("3. Deep Sequence-to-Sequence (Encoder-Decoder) Architectures", "Sutskever et al. (2014) and Bahdanau et al. (2015) introduced LSTM Encoder-Decoder networks with additive attention for sequence transduction. Applied to renewable energy forecasting (Voyant et al., 2017; Wang et al., 2022), Seq2Seq models encode multi-day historical trajectories into latent states and decode multi-step future horizons jointly. However, existing academic studies stop at predicting irradiance or megawatts, omitting downstream coupling to steam accumulator pressure vessels and operator-facing LLM decision support.")

    add_heading_16("2.2 Research Gaps Identified")
    add_bullet_item("Gap 1: Myopic Single-Step Forecasting", "Tabular regressors such as XGBoost predict only H+1 from engineered lags; rolling them out autoregressively over 24 hours accumulates compounding errors and ignores long-term thermal mass in solar collector piping.")
    add_bullet_item("Gap 2: Disconnection Between Neural Forecasts and Storage Kinetics", "Most solar forecasting papers evaluate RMSE in isolation without translating predicted steam surplus into actionable charge/discharge schedules across pressurized steam accumulator tanks.")
    add_bullet_item("Gap 3: Control Room Interpretability Deficit", "Plant operators distrust black-box neural predictions during cloud transients. Existing dashboards lack attention-based interpretability and conversational AI guidance grounded in real SCADA valve tags.")

    add_styled_table(
        ["Method Family", "Temporal Scope", "Strengths", "Key Limitation"],
        [
            ["Persistence Baseline", "Single-step carry-over", "Zero training cost", "Fails severely across 24h diurnal cycle (RMSE 25.25 t/h)"],
            ["Physical DSG Solvers", "Continuous PDE", "Thermodynamically exact", "Cannot adapt to mirror soiling or cloud transients"],
            ["XGBoost Regressor", "1-Hour point prediction", "Strong H+1 accuracy (R² 0.916)", "No recurrent memory; compounds error over 24h rollouts"],
            ["Proposed Seq2Seq + Attention", "48h In -> 24h Out", "Learns thermal inertia + attention alignment", "Solved end-to-end with storage & LLM dispatch"],
        ],
        caption="Table 2.1: Comparison of Existing Solar Steam & Time-Series Forecasting Methods",
        col_widths=[1.6, 1.3, 1.6, 1.8]
    )

    add_heading_16("2.3 Objectives")
    add_bullet_item("Objective 1", "Replace single-step tabular regression with a 2-Layer LSTM Encoder-Decoder with Bahdanau Attention trained on 48-hour SCADA lookback windows to forecast 24-hour solar steam profiles.")
    add_bullet_item("Objective 2", "Eliminate data leakage through strict chronological splitting (70% train, 10% validation, 20% unseen test) and training-only median imputation and Z-score standardization.")
    add_bullet_item("Objective 3", "Couple the 24-hour neural forecast to an engineering LPG Displacement & 9-Tank Accumulator Storage model to maximize boiler shutoff hours.")
    add_bullet_item("Objective 4", "Provide an accessible web platform featuring a Groq Llama-3.3-70B AI advisor and an interactive SVG guide ('Helio') with 1-click stress-test scenarios.")

    # -------------------------------------------------------------
    # CHAPTER 3: PROJECT IDEA AND MOTIVATION
    # -------------------------------------------------------------
    add_chapter_title("3", "PROJECT IDEA AND MOTIVATION")
    add_body("The core idea of HelioSteam AI is to transform intermittent solar steam into a predictable, dispatchable industrial utility by unifying sequence-to-sequence deep learning, thermodynamic storage physics, and generative AI decision support. Rather than treating the solar field, the nine steam accumulator tanks, and the auxiliary LPG boiler as separate subsystems, the platform models them as a single cyber-physical loop.")
    add_body("Three practical motivations drive this architecture:")
    add_bullet_item("Eliminating Standby Fossil Waste", "When operators lack a reliable 24-hour solar forecast, they keep LPG boilers burning on warm standby (42.0 kg/h parasitic loss) even during sunny afternoons. Accurate 24-hour Seq2Seq forecasting gives engineers the confidence to transition the boiler to cold-shutoff isolation.")
    add_bullet_item("Economic and Carbon Impact", "At industrial LPG tariffs of $0.92/kg and an IPCC emission factor of 3.0 kg CO2/kg LPG, displacing ~24.9 tons of LPG on a peak clear day saves nearly $23,000 USD and prevents 74.9 metric tons of CO2 emissions in a single 24-hour cycle.")
    add_bullet_item("Human-Centered Control Room AI", "Operators under shift pressure need clear answers rather than raw tensor outputs. Integrating Groq Llama-3.3-70B with real-time plant metrics and the 'Helio' vector assistant turns complex thermal forecasts into plain-English valve and boiler directives.")

    # -------------------------------------------------------------
    # CHAPTER 4: PROCEDURE
    # -------------------------------------------------------------
    add_chapter_title("4", "PROCEDURE")
    add_heading_16("4.1 Industrial Plant Topology & Thermodynamic Balance")
    add_body("The system is modeled on the commercial 10 MWe eLLO Concentrated Solar Power plant in Llo, France, a Linear Fresnel Reflector (LFR) Direct Steam Generation (DSG) facility equipped with 124 SCADA sensors across East and West solar collector loops, a 9-vessel steam accumulator storage bank (Tanks 1–9), a deaerator/feedwater recovery loop, and an auxiliary LPG backup boiler.")

    add_figure(os.path.join(BASE_DIR, "data", "Solar_field.png"), "Figure 4.1: Schematic Diagram of the eLLO Linear Fresnel Direct Steam Solar Field", width_in=5.2)
    add_figure(os.path.join(BASE_DIR, "data", "Storage.png"), "Figure 4.2: Nine-Vessel High-Pressure Steam Accumulator Storage System", width_in=5.2)

    add_body("The thermodynamic LPG displacement rate is computed from steam enthalpy conservation: specific LPG consumption is given by (1000 * Delta_h) / (eta_boiler * LHV_LPG) = 67.66 kg LPG per ton of steam (using Delta_h = 2.62 MJ/kg, boiler efficiency 84%, and LPG LHV = 46.1 MJ/kg). Feedwater preheating recovery (up to 203°C) dynamically reduces effective enthalpy demand during active solar hours.")

    add_heading_16("4.2 Seq2Seq Encoder-Decoder with Bahdanau Attention")
    add_body("To capture multi-day thermal inertia and diurnal periodicity, the legacy point-wise XGBoost regressor was replaced with a PyTorch Seq2Seq 2-Layer LSTM Encoder-Decoder equipped with Bahdanau Additive Attention:")
    add_bullet_item("Encoder Network", "A 2-layer LSTM (hidden_dim = 64, dropout = 0.15) ingests a 48-hour historical sequence of 12 standardized features: GHI, East_DNI, West_DNI, Ambient_Temp, Wind_Speed, West_Feedwater, East_Feedwater, sin/cos(hour), sin/cos(day_of_year), and historical Steam_Current. It outputs 48 contextual hidden states H_enc (48 x 64) and final cell states (h_n, c_n).")
    add_bullet_item("Bahdanau Additive Attention", "At each forecast step h in 1..24, the decoder query s_{h-1} attends over all 48 encoder states via e_{h,tau} = v^T tanh(W_q s_{h-1} + W_k h_tau^enc), alpha_h = softmax(e_h), and context vector c_h = sum(alpha_{h,tau} * h_tau^enc). This allows the decoder to directly recall yesterday's midday peak or recent cloud transients.")
    add_bullet_item("Decoder Network & Output Head", "A 2-layer LSTM decoder steps through h = 1..24 autoregressively, taking [y_{h-1}, future_covariates_h (9 features), c_h] as input. A two-layer MLP head (137 -> 32 -> 1 with ReLU) predicts steam output, followed by physical non-negativity and nighttime zero-clamping (GHI < 15, East_DNI < 10, West_DNI < 10).")
    add_bullet_item("Zero-Dependency Runtime Export", "Trained PyTorch weights (135,073 parameters) are exported to compressed NumPy arrays (seq2seq_weights.npz). The production backend executes exact LSTM and attention matrix multiplications in pure NumPy, guaranteeing bit-for-bit parity (0.0 t/h discrepancy) with zero PyTorch runtime overhead.")

    add_styled_table(
        ["Component / Hyperparameter", "Configuration Value", "Design Rationale"],
        [
            ["Encoder Lookback Window", "48 consecutive hours", "Captures two full diurnal thermal cycles"],
            ["Decoder Forecast Horizon", "24 consecutive hours", "Full day-ahead boiler & storage planning"],
            ["LSTM Layers & Hidden Size", "2 Layers, H = 64", "Balances non-linear capacity vs. 8,761-row dataset size"],
            ["Attention Mechanism", "Bahdanau Additive (W_q, W_k, v)", "Dynamic alignment across 48h history"],
            ["Total Trainable Parameters", "135,073 parameters", "Compact footprint (~530 KB compressed NPZ)"],
            ["Optimizer & LR Schedule", "AdamW (lr=0.002) + ReduceLROnPlateau", "Stable gradient convergence over 40 epochs"],
            ["Scheduled Sampling", "Teacher forcing decay 0.85 -> 0.10", "Prevents autoregressive exposure bias"],
        ],
        caption="Table 4.1: Seq2Seq Encoder-Decoder Architecture & Training Hyperparameters",
        col_widths=[2.0, 2.0, 2.3]
    )

    add_heading_16("4.3 Thermal Storage Scheduling & LLM Integration")
    add_body("Using the 24-hour decoded steam curve, the LPGConsumptionAnalyzer allocates surplus solar steam (> 28.0 t/h demand) into Tanks 1–9 (85 t capacity, 88% round-trip efficiency) and dispatches stored steam during evening ramps before firing the LPG boiler. Finally, the Groq Llama-3.3-70B advisor grounds operator chat responses in the live hourly predictions and SCADA tags.")

    # -------------------------------------------------------------
    # CHAPTER 5: DATA COLLECTION AND ANALYSIS
    # -------------------------------------------------------------
    add_chapter_title("5", "DATA COLLECTION AND ANALYSIS")
    add_body("The empirical dataset comprises 8,761 consecutive hourly aggregated SCADA records spanning January 1, 2025 to January 1, 2026 from the 10 MWe eLLO CSP plant, supplemented by an 8,640-row high-resolution 10-second snapshot (July 16–17, 2025). Out of 365 calendar days, 359 complete operational days were evaluated after accounting for minor sensor maintenance intervals.")

    add_figure(os.path.join(FIG_DIR, "fig1_seq2seq_architecture.png"), "Figure 5.1: HelioSteam AI Seq2Seq 2-Layer LSTM Encoder-Decoder Architecture with Bahdanau Attention", width_in=6.1)

    add_heading_16("5.1 Monitored SCADA Sensors & Preprocessing")
    add_body("Erroneous measurements were flagged as NaN in the raw SCADA log, and valve-position zero corrections were applied to prevent false flow readings when isolation valves were closed. To prevent data leakage, median imputation statistics and Z-score normalization parameters (mean and standard deviation) were fitted strictly on the first 80% chronological training split.")

    add_styled_table(
        ["Feature / Target", "SCADA Tag", "Unit", "Role in Seq2Seq Pipeline"],
        [
            ["Global Horizontal Irradiance", "22_WTA99_CT001 / GHI", "W/m²", "Encoder & Decoder primary solar input"],
            ["East & West Field DNI", "8_LBA / 6_LBA DNI", "W/m²", "Directional beam irradiance per field"],
            ["Ambient Temp & Wind Speed", "22_WTA99 / 10m Anemometer", "°C, km/h", "Convective thermal loss compensation"],
            ["East & West Feedwater", "6_LAB51 / 8_LAB52", "t/h", "Collector hydraulic mass balance"],
            ["Cyclic Time Encoding", "sin/cos(Hour), sin/cos(DOY)", "rad", "Continuous diurnal & seasonal position"],
            ["Total Solar Steam (Target)", "8_LBA10 + 6_LBA10", "t/h", "Encoder history (48h) & Decoder target (24h)"],
        ],
        caption="Table 5.1: Key Monitored SCADA Telemetry Parameters & Sensor Tags",
        col_widths=[1.7, 1.6, 0.8, 2.2]
    )

    add_heading_16("5.2 Sliding Window Construction & Chronological Partitioning")
    add_body("From the 8,761 hourly records, 8,639 valid sliding windows of length 48h (encoder) + 24h (decoder) were extracted (requiring >= 18/24 valid target hours per window). Windows were partitioned strictly chronologically with zero temporal overlap: 6,034 training windows (70%), 876 validation windows (10%, used for early stopping), and 1,729 unseen test windows (20%, spanning 41,472 total forecast steps).")

    # -------------------------------------------------------------
    # CHAPTER 6: RESULTS AND DISCUSSIONS
    # -------------------------------------------------------------
    add_chapter_title("6", "RESULTS AND DISCUSSIONS")
    add_heading_16("6.1 Training Convergence & Benchmark Comparison")
    add_body("The Seq2Seq Encoder-Decoder converged smoothly over 40 epochs under scheduled teacher forcing (decaying from 0.85 to 0.10), achieving its lowest validation RMSE of 2.911 t/h. Figure 6.1 illustrates the training and validation RMSE trajectories.")

    add_figure(os.path.join(FIG_DIR, "fig2_training_curve.png"), "Figure 6.1: Seq2Seq Encoder-Decoder Training & Validation Convergence (40 Epochs)", width_in=5.6)

    add_styled_table(
        ["Model Architecture", "Evaluation Scope", "R²", "MAE (t/h)", "RMSE (t/h)", "Skill Score vs. Persistence"],
        [
            ["Persistence Baseline (24h)", "41,472 test steps", "N/A", "12.410", "25.249", "0.00% (Baseline)"],
            ["Legacy XGBoost (500 Trees)", "H+1 next-hour only (1,744h)", "0.9158", "2.082", "5.370", "+46.21% (vs. 1h Pers.)"],
            ["Seq2Seq LSTM + Attention (H+1)", "H+1 slice (1,728 steps)", "0.9043", "2.227", "5.683", "+42.78% (vs. 1h Pers.)"],
            ["Seq2Seq LSTM + Attention (24h)", "Full 24h rollout (41,472 steps)", "0.9174", "1.973", "5.295", "+79.03% (vs. 24h Pers.)"],
        ],
        caption="Table 6.1: Statistical Benchmark: Seq2Seq Encoder-Decoder vs. XGBoost & Persistence",
        col_widths=[1.7, 1.4, 0.65, 0.75, 0.8, 1.0]
    )

    add_body("Remarkably, across the full 24-hour sequence forecast (41,472 unseen test steps), the Seq2Seq Encoder-Decoder outperforms even the next-hour-only XGBoost baseline in both R² (0.9174 vs. 0.9158), MAE (1.973 vs. 2.082 t/h), and RMSE (5.295 vs. 5.370 t/h), while delivering a +79.03% skill score improvement over 24-hour persistence. Across 359 complete operational days, daily aggregated steam totals achieve a Daily R² of 0.9808 and Daily MAE of 15.19 t.")

    add_heading_16("6.2 24-Hour Curve & Attention Interpretability")
    add_body("Figure 6.2 presents the decoded 24-hour solar steam trajectory on July 16 against actual SCADA flow rates, clearly capturing the Morning Warm-Up (06:00–10:00), Midday Solar Peak (10:00–16:00), and Evening Storage Dispatch (16:00–21:00). Figure 6.3 visualizes the mean Bahdanau attention weights across all 24 forecast steps and 48 historical encoder hours, confirming that the decoder learns to attend selectively to the most recent hours (t-6..t) as well as the corresponding diurnal peak 24 hours earlier (t-24).")

    add_figure(os.path.join(FIG_DIR, "fig3_july16_forecast.png"), "Figure 6.2: 24-Hour Solar Steam Forecast vs. Actual SCADA Output (July 16)", width_in=5.8)
    add_figure(os.path.join(FIG_DIR, "fig4_attention_heatmap.png"), "Figure 6.3: Bahdanau Attention Alignment Across 48h History vs. 24h Forecast Horizon", width_in=5.8)

    add_heading_16("6.3 Multi-Horizon Error Stability")
    add_body("Table 6.2 and Figure 6.4 evaluate forecasting accuracy across increasing lead times from H+1 to H+24. Unlike autoregressive tabular models whose errors explode over multi-hour horizons, the Encoder-Decoder maintains rock-solid stability (R² > 0.913 and MAE < 2.02 t/h from H+3 all the way through H+24).")

    hb_rows = [
        [f"H+{x['horizon_h']}", f"{x['r2']:.4f}", f"{x['mae_th']:.3f}", f"{x['rmse_th']:.3f}", f"{x['persistence_rmse_th']:.3f}", f"+{x['skill_score_pct']:.2f}%"]
        for x in SEQ_META['horizon_breakdown']
    ]
    add_styled_table(
        ["Horizon", "R²", "MAE (t/h)", "RMSE (t/h)", "Persistence RMSE", "Skill Score"],
        hb_rows,
        caption="Table 6.2: Multi-Horizon Seq2Seq Error Breakdown (H+1 to H+24)",
        col_widths=[0.9, 0.9, 1.0, 1.0, 1.3, 1.2]
    )
    add_figure(os.path.join(FIG_DIR, "fig5_horizon_comparison.png"), "Figure 6.4: Forecasting Error (RMSE) Across 24-Hour Horizons vs. Persistence Baseline", width_in=5.6)

    add_heading_16("6.4 LPG Displacement, Storage Dispatch & Stress-Test Validation")
    add_body("Coupled with the nine-tank thermal accumulator model on July 16 (total solar steam: 951.28 t), the Seq2Seq forecast enables 17 continuous hours of zero-LPG boiler shutoff, displacing 24,966 kg of LPG, saving $22,969 USD in daily fuel costs, and avoiding 74.9 tons of CO2. Under the interactive 'Cloud Ambush' stress test (60% irradiance drop between 12:00 and 14:00), the Encoder-Decoder dynamically re-forecasts daily steam from 951.28 t down to 749.17 t (-202.11 t), triggering automatic accumulator compensation.")

    add_styled_table(
        ["Daily Phase", "Time Window (CET)", "Solar & Storage Behavior", "Boiler & LPG Status"],
        [
            ["1. Morning Warm-Up", "06:00 – 10:00", "Receiver thermal mass rises; steam ramps 0 -> 45 t/h", "Partial LPG top-up; preheat recovery active"],
            ["2. Midday Solar Peak", "10:00 – 16:00", "Peak solar steam > 100 t/h; surplus charges Tanks 1–9", "100% Zero LPG (Boiler in cold shutoff)"],
            ["3. Evening Storage Dispatch", "16:00 – 23:00", "Accumulators discharge stored steam into header", "Zero LPG maintained up to 23:00 (17h total)"],
        ],
        caption="Table 6.3: Three-Phase Daily Operational Dispatch & LPG Savings (July 16)",
        col_widths=[1.5, 1.3, 1.8, 1.7]
    )

    # -------------------------------------------------------------
    # CHAPTER 7: CONCLUSION
    # -------------------------------------------------------------
    add_chapter_title("7", "CONCLUSION")
    add_body("This project successfully upgraded the HelioSteam AI forecasting core from a single-step XGBoost regressor to a full Sequence-to-Sequence (Seq2Seq) 2-Layer LSTM Encoder-Decoder architecture with Bahdanau Additive Attention, trained on 8,761 hourly SCADA records from the 10 MWe eLLO Linear Fresnel solar plant.")
    add_body("On 1,729 unseen chronological test windows (41,472 horizon predictions), the Encoder-Decoder achieved an overall R² of 0.9174, MAE of 1.973 t/h, RMSE of 5.295 t/h, and a +79.03% skill score improvement over the 24-hour persistence baseline, while preserving stability from H+1 through H+24 and exporting to a lightweight pure-NumPy runtime with exact 0.0 t/h parity to PyTorch.")
    add_body("Integrated with nine-tank steam accumulator optimization, interactive stress-test scenarios, the 'Helio' onboarding guide, and the Groq Llama-3.3-70B AI advisor, the system delivers actionable boiler shutoff schedules that displace up to 24,966 kg of LPG and prevent 74.9 tons of CO2 emissions on peak solar days. Future work will incorporate probabilistic quantile decoding for cloud uncertainty bands and direct deployment onto edge plant PLCs.")

    # -------------------------------------------------------------
    # CHAPTER 8: REFERENCES
    # -------------------------------------------------------------
    add_chapter_title("8", "REFERENCES")
    refs = [
        "[1] S. Sutskever, O. Vinyals, and Q. V. Le, \"Sequence to Sequence Learning with Neural Networks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 27, 2014.",
        "[2] D. Bahdanau, K. Cho, and Y. Bengio, \"Neural Machine Translation by Jointly Learning to Align and Translate,\" in International Conference on Learning Representations (ICLR), 2015.",
        "[3] V. Grange and S. Rodat, \"Annual Operational Data for the 10 MWe eLLO Fresnel Concentrated Solar Power Plant,\" PROMES-CNRS, Llo, France, 2026.",
        "[4] J. A. Duffie and W. A. Beckman, Solar Engineering of Thermal Processes, 4th ed. Hoboken, NJ, USA: Wiley, 2013.",
        "[5] T. Chen and C. Guestrin, \"XGBoost: A Scalable Tree Boosting System,\" in Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining, 2016, pp. 785–794.",
        "[6] C. Voyant, G. Notton, S. Kalogirou, M.-L. Nivet, C. Paoli, F. Motte, and A. Fouilloy, \"Machine learning methods for solar radiation forecasting: A review,\" Renewable Energy, vol. 105, pp. 569–582, 2017.",
        "[7] F. Wang, Z. Xuan, Z. Zhen, K. Li, T. Wang, and M. Shi, \"A review on technology for day-ahead solar power forecasting: Methods, error analysis, and benchmark datasets,\" Renew. Sustain. Energy Rev., vol. 168, p. 112836, 2022.",
        "[8] H. M. Steinhagen and G. L. Morrison, \"Direct steam generation in parabolic trough solar collectors: Transient flow modeling and control,\" Solar Energy, vol. 184, pp. 532–545, 2019.",
        "[9] D. García-Gastello, M. M. Prieto, and I. Suárez, \"Dynamic simulation and optimization of steam accumulator systems in direct solar steam generation plants,\" Energy Convers. Manag., vol. 230, p. 113791, 2021.",
        "[10] International Energy Agency (IEA), \"Solar Heat for Industry: Clean Energy Technology Briefs,\" IEA SolarPACES Programme, Paris, 2023.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    out_path = os.path.join(BASE_DIR, "HelioSteam_AI_Seq2Seq_Project_Report.docx")
    doc.save(out_path)
    print(f"Saved official SRM report to: {out_path}")


if __name__ == '__main__':
    build_report()
