import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PPT = os.path.join(BASE_DIR, 'existing_autoencoder_ppt.pptx')
OUT_PPT = os.path.join(BASE_DIR, 'Autoencoders_Solar_Steam_CaseStudy_Presentation.pptx')
FIG_DIR = os.path.join(BASE_DIR, 'report_figures')

NAVY = RGBColor(15, 23, 42)
SLATE = RGBColor(71, 85, 105)
EMERALD = RGBColor(5, 150, 105)
EMERALD_BG = RGBColor(236, 253, 245)
BLUE = RGBColor(37, 99, 235)
BLUE_BG = RGBColor(239, 246, 255)
AMBER = RGBColor(217, 119, 6)
AMBER_BG = RGBColor(255, 251, 235)
LIGHT_BG = RGBColor(248, 250, 252)
BORDER = RGBColor(203, 213, 225)
WHITE = RGBColor(255, 255, 255)


def move_slide(prs, old_index, new_index):
    xml_slides = prs.slides._sldIdLst
    slides = list(xml_slides)
    el = slides[old_index]
    xml_slides.remove(el)
    xml_slides.insert(new_index, el)


def style_bg_and_header(slide, title, subtitle, page_num):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = LIGHT_BG

    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.22), Inches(9.0), Inches(0.48))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = NAVY

    sb = slide.shapes.add_textbox(Inches(0.5), Inches(0.68), Inches(9.0), Inches(0.32))
    stf = sb.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = subtitle
    sp.font.size = Pt(12)
    sp.font.color.rgb = SLATE

    nb = slide.shapes.add_textbox(Inches(8.7), Inches(5.22), Inches(0.8), Inches(0.3))
    np_ = nb.text_frame.paragraphs[0]
    np_.alignment = PP_ALIGN.RIGHT
    np_.text = str(page_num)
    np_.font.size = Pt(10)
    np_.font.color.rgb = SLATE


def add_card(slide, x, y, w, h, title, bullets, bg_col=WHITE, bd_col=BORDER, title_col=NAVY):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = bg_col
    sh.line.color.rgb = bd_col
    sh.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(Inches(x + 0.14), Inches(y + 0.10), Inches(w - 0.28), Inches(h - 0.20))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = title_col
    p0.space_after = Pt(4)

    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY
        p.space_after = Pt(3)


def main():
    prs = Presentation(SRC_PPT)
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1]

    # Update Slide 13 ("Key takeaways") page number to 17
    last_slide = prs.slides[12]
    for sh in last_slide.shapes:
        if sh.has_text_frame and sh.text.strip() == '13':
            sh.text_frame.paragraphs[0].text = '17'

    # ---------------------------------------------------------
    # NEW SLIDE 13: Case Study Implementation
    # ---------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    style_bg_and_header(
        s13,
        "Case Study: Solar Steam Forecasting (HelioSteam AI)",
        "Applying Encoder-Decoder sequence learning to a 10 MWe Linear Fresnel DSG solar plant (8,761 hourly SCADA rows)",
        13
    )
    fig1 = os.path.join(FIG_DIR, 'fig1_seq2seq_architecture.png')
    if os.path.exists(fig1):
        s13.shapes.add_picture(fig1, Inches(0.45), Inches(1.05), width=Inches(9.1))

    add_card(s13, 0.45, 3.92, 2.9, 1.22, "48h Encoder (History)", [
        "2-layer LSTM (H=64) encodes 12 features",
        "Captures collector pipe thermal inertia"
    ], bg_col=BLUE_BG, bd_col=BLUE, title_col=BLUE)
    add_card(s13, 3.55, 3.92, 2.9, 1.22, "Bahdanau Attention", [
        "Aligns each forecast step to past 48h",
        "Recalls yesterday's peak & cloud dips"
    ], bg_col=AMBER_BG, bd_col=AMBER, title_col=AMBER)
    add_card(s13, 6.65, 3.92, 2.9, 1.22, "24h Decoder -> LPG Plan", [
        "Decodes 24h steam + 9 future covariates",
        "Drives 9-tank storage & Groq AI chat"
    ], bg_col=EMERALD_BG, bd_col=EMERALD, title_col=EMERALD)

    # ---------------------------------------------------------
    # NEW SLIDE 14: Case Study Results & Attention Interpretability
    # ---------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    style_bg_and_header(
        s14,
        "Case Study Results: 24h Steam Forecast & Attention Map",
        "Chronological unseen test evaluation (1,729 windows / 41,472 steps) + July 16 plant dispatch",
        14
    )
    fig3 = os.path.join(FIG_DIR, 'fig3_july16_forecast.png')
    fig4 = os.path.join(FIG_DIR, 'fig4_attention_heatmap.png')
    if os.path.exists(fig3):
        s14.shapes.add_picture(fig3, Inches(0.45), Inches(1.08), width=Inches(4.45))
    if os.path.exists(fig4):
        s14.shapes.add_picture(fig4, Inches(5.08), Inches(1.08), width=Inches(4.47))

    add_card(s14, 0.45, 3.85, 2.15, 1.25, "951.28 t / day", ["Peak July 16 solar steam output"], bg_col=EMERALD_BG, bd_col=EMERALD, title_col=EMERALD)
    add_card(s14, 2.75, 3.85, 2.15, 1.25, "17 Hours OFF", ["Continuous zero-LPG boiler shutoff"], bg_col=EMERALD_BG, bd_col=EMERALD, title_col=EMERALD)
    add_card(s14, 5.05, 3.85, 2.15, 1.25, "24,966 kg LPG", ["Daily fossil fuel displaced ($22,969)"], bg_col=AMBER_BG, bd_col=AMBER, title_col=AMBER)
    add_card(s14, 7.35, 3.85, 2.20, 1.25, "74.9 t CO₂", ["Emissions avoided on a sunny day"], bg_col=BLUE_BG, bd_col=BLUE, title_col=BLUE)

    # ---------------------------------------------------------
    # NEW SLIDE 15: Multi-Model Comparison (Case-Study Metrics)
    # ---------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    style_bg_and_header(
        s15,
        "Model Comparison: Case-Study-Specific Metrics",
        "Evaluated on identical unseen test split (41,472 steps) — focusing on steam & LPG errors, not just accuracy",
        15
    )

    headers = ["Model Architecture", "Hourly MAE\n(t/h) ↓", "Hourly RMSE\n(t/h) ↓", "Steam R²\n↑", "24h Skill\nScore ↑", "Daily Steam\nMAE (t/d) ↓", "Daily LPG\nError (kg/d) ↓"]
    rows_data = [
        ["24h Persistence Baseline", "12.005", "25.249", "-0.8771", "0.00%", "261.97", "17,724.9"],
        ["Dense (MLP) Enc-Dec", "2.384", "6.044", "0.8924", "+76.06%", "47.89", "3,240.0"],
        ["1D-CNN Enc-Dec", "2.290", "5.765", "0.9021", "+77.17%", "50.31", "3,404.2"],
        ["GRU Enc-Dec (No Attn)", "1.919", "5.234", "0.9193", "+79.27%", "40.90", "2,767.0"],
        ["XGBoost (H+1 Tabular only)", "2.082", "5.370", "0.9158", "+46.21% (1h)", "14.63", "989.9"],
        ["LSTM + Bahdanau Attn (Ours)", "1.973", "5.295", "0.9174", "+79.03%", "15.19", "1,027.8"],
    ]

    tbl_shape = s15.shapes.add_table(len(rows_data) + 1, len(headers), Inches(0.45), Inches(1.12), Inches(9.1), Inches(3.25))
    tbl = tbl_shape.table
    col_ws = [2.45, 1.05, 1.1, 0.95, 1.15, 1.15, 1.25]
    for j, w in enumerate(col_ws):
        tbl.columns[j].width = Inches(w)

    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = WHITE

    for i, rdata in enumerate(rows_data, start=1):
        is_ours = (i == len(rows_data))
        for j, val in enumerate(rdata):
            cell = tbl.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = EMERALD_BG if is_ours else (WHITE if i % 2 == 1 else LIGHT_BG)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = val
            r.font.size = Pt(9.5)
            r.font.bold = is_ours
            r.font.color.rgb = EMERALD if (is_ours and j > 0) else NAVY

    add_card(
        s15, 0.45, 4.48, 9.1, 0.68,
        "Why Case-Study Metrics Matter:",
        ["While GRU & 1D-CNN achieve decent hourly RMSE, our LSTM + Bahdanau Attention cuts Daily Cumulative Steam MAE by 63% (15.19 vs. 40.90 t/d), keeping daily LPG estimation error within ~1,028 kg/day for reliable boiler scheduling."],
        bg_col=AMBER_BG, bd_col=AMBER, title_col=AMBER
    )

    # ---------------------------------------------------------
    # NEW SLIDE 16: Visual Comparison & Operational Insight
    # ---------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    style_bg_and_header(
        s16,
        "Visual Benchmark: Hourly vs. Daily Operational Error",
        "Comparing 6 architectures on both instantaneous steam error (RMSE) and daily cumulative boiler dispatch error",
        16
    )
    fig6 = os.path.join(FIG_DIR, 'fig6_model_comparison.png')
    if os.path.exists(fig6):
        s16.shapes.add_picture(fig6, Inches(0.45), Inches(1.05), width=Inches(9.1))

    add_card(s16, 0.45, 4.02, 2.9, 1.12, "Beats MLP & 1D-CNN", [
        "12–16% lower hourly RMSE",
        "68% lower daily LPG error"
    ], bg_col=WHITE, bd_col=BORDER, title_col=BLUE)
    add_card(s16, 3.55, 4.02, 2.9, 1.12, "Beats GRU (No Attn)", [
        "Similar hourly RMSE (~5.3 t/h)",
        "2.7x better daily steam total"
    ], bg_col=WHITE, bd_col=BORDER, title_col=AMBER)
    add_card(s16, 6.65, 4.02, 2.9, 1.12, "Beats Single-Step XGBoost", [
        "True 24h sequence forecast",
        "+79.03% 24h skill score"
    ], bg_col=EMERALD_BG, bd_col=EMERALD, title_col=EMERALD)

    # Reorder so new slides (indices 13,14,15,16) sit right before "Key takeaways" (index 12)
    # Current order: 0..11 (slides 1..12), 12 (takeaways), 13..16 (new 4 slides)
    # Move index 12 to the very end (index 16)
    move_slide(prs, 12, 16)

    prs.save(OUT_PPT)
    print(f"Saved combined presentation ({len(prs.slides)} slides) to: {OUT_PPT}")


if __name__ == '__main__':
    main()
