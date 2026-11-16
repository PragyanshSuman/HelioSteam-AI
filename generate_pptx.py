import os
import sys

def create_presentation():
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_DARK = RGBColor(9, 18, 29)
    CARD_BG = RGBColor(18, 32, 51)
    CARD_BORDER = RGBColor(38, 56, 82)
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    TEXT_AMBER = RGBColor(245, 158, 11)
    TEXT_GREEN = RGBColor(16, 185, 129)
    TEXT_RED = RGBColor(239, 68, 68)

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, subtitle):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEXT_AMBER

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.65))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Subtitle
        s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.4))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.size = Pt(13)
        p_s.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, body_bullets, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.size = Pt(15)
            p0.font.bold = True
            p0.font.color.rgb = TEXT_WHITE
            p0.space_after = Pt(10)

        for i, b in enumerate(body_bullets):
            p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
            p.text = "• " + b
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MUTED
            p.space_after = Pt(8)

    def add_stat_box(slide, left, top, width, height, value, label, sub=""):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER

        tb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.15), width - Inches(0.2), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = value
        p1.alignment = PP_ALIGN.CENTER
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_GREEN

        p2 = tf.add_paragraph()
        p2.text = label
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

        if sub:
            p3 = tf.add_paragraph()
            p3.text = sub
            p3.alignment = PP_ALIGN.CENTER
            p3.font.size = Pt(9)
            p3.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    tbox = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.33), Inches(3.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "☀️ INDUSTRIAL AI & GREEN THERMAL ENERGY"
    p_badge.alignment = PP_ALIGN.CENTER
    p_badge.font.size = Pt(12)
    p_badge.font.bold = True
    p_badge.font.color.rgb = TEXT_AMBER
    p_badge.space_after = Pt(14)

    p_hero = tf1.add_paragraph()
    p_hero.text = "HelioSteam AI Platform"
    p_hero.alignment = PP_ALIGN.CENTER
    p_hero.font.size = Pt(40)
    p_hero.font.bold = True
    p_hero.font.color.rgb = TEXT_WHITE
    p_hero.space_after = Pt(10)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Daily Solar Steam Production Forecasting & LLM-Driven LPG Optimization for Industrial Plants"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(24)

    p_author = tf1.add_paragraph()
    p_author.text = "Presenter: Sanjai Guru | Direct Solar Steam Generation (DSG) | XGBoost & Groq AI"
    p_author.alignment = PP_ALIGN.CENTER
    p_author.font.size = Pt(12)
    p_author.font.bold = True
    p_author.font.color.rgb = TEXT_GREEN

    s1.notes_slide.notes_text_frame.text = (
        "Good morning everyone. Today, I am proud to present HelioSteam AI. "
        "This project bridges machine learning with industrial thermal engineering to solve a multi-million-dollar challenge: "
        "how manufacturing factories can dependably use free solar steam to replace expensive, polluting LPG fossil fuel boilers."
    )

    # ==========================================
    # SLIDE 2: Problem Statement
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Problem Statement", "The Industrial Dilemma: Clean Solar vs. Reliable Steam", "Why factories burn expensive fossil fuel even when solar collectors are installed")

    add_card(s2, Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7), "⚠️ The Industrial Constraint", [
        "24/7 Continuous Demand: Textiles, pharma, and food processing cannot tolerate steam drops.",
        "Production Risk: A 10-minute steam pressure loss halts manufacturing lines, costing thousands of dollars.",
        "Unpredictable Sunlight: Passing clouds or dust create sudden drops in solar steam output.",
        "The 'Fear Factor': Plant operators keep auxiliary LPG boilers burning on standby 24/7 out of caution."
    ], border_color=TEXT_RED)

    add_card(s2, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.7), "💸 The Costly Consequences", [
        "Massive Fuel Consumption: Auxiliary boilers burn tons of expensive LPG unnecessarily.",
        "Heavy Carbon Footprint: Continuous fossil fuel combustion releases severe CO2 emissions.",
        "Hardware Underutilization: Multi-million dollar solar fields sit underutilized because humans cannot foresee cloud patterns.",
        "Need for Smart Software: Clean hardware alone is not enough—plants need predictive intelligence."
    ], border_color=TEXT_AMBER)

    s2.notes_slide.notes_text_frame.text = (
        "Factories need boiling steam non-stop. Solar mirrors give free, green steam—but the sun is unpredictable. "
        "A single cloud cuts steam output. Because factories cannot stop their machines, operators leave fossil fuel boilers running on standby all day long out of fear. "
        "This wastes over 24,000 kg of gas every day and emits massive carbon pollution."
    )

    # ==========================================
    # SLIDE 3: Project Objectives
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Project Objectives", "Four Strategic Goals for Sustainable Steam", "Uniting machine learning prediction, storage kinetics, and operator decision-support")

    add_card(s3, Inches(0.8), Inches(2.2), Inches(2.7), Inches(4.5), "1. Predict Ahead", [
        "Forecast solar steam 1 hour and 24 hours in advance.",
        "Utilize live SCADA sensor feeds and irradiance telemetry."
    ])
    add_card(s3, Inches(3.8), Inches(2.2), Inches(2.7), Inches(4.5), "2. Displace LPG", [
        "Identify exact hours solar output exceeds factory demand.",
        "Safely isolate auxiliary boilers to eliminate standby losses."
    ])
    add_card(s3, Inches(6.8), Inches(2.2), Inches(2.7), Inches(4.5), "3. Optimize Storage", [
        "Schedule charging of 9 steam accumulator pressure vessels.",
        "Discharge stored thermal mass to cover peak evening hours."
    ])
    add_card(s3, Inches(9.8), Inches(2.2), Inches(2.7), Inches(4.5), "4. Simplify Control", [
        "Interactive SVG guide ('Helio') walks operators through decisions.",
        "Groq LLM gives plain-English technical procedures."
    ])

    s3.notes_slide.notes_text_frame.text = (
        "Our project had four key objectives: First, predict solar steam output 1 hour and 24 hours ahead. "
        "Second, calculate exactly when the operator can safely shut off the LPG boiler. "
        "Third, optimize the plant's 9 thermal accumulator storage tanks so solar steam stored in the afternoon covers the night shift. "
        "And fourth, wrap everything in an intuitive UI with a character mascot and AI chat so any operator can use it without confusion."
    )

    # ==========================================
    # SLIDE 4: Architecture & Dataset
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Plant Architecture & Data", "Direct Solar Steam (DSG) Plant & SCADA Telemetry", "Trained and evaluated on 8,760 hours of real industrial telemetry")

    add_card(s4, Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7), "🏭 Physical Plant Assets", [
        "Solar Collector Field: East Field (Loops 1–10) + West Field (Loops 11–27) parabolic troughs.",
        "Thermal Storage System: 9 high-pressure steam accumulator vessels (Tanks 1–9) operating at 62 barg.",
        "Auxiliary Fossil Boiler: Backup LPG boiler supplying up to 28.0 t/h peak steam demand.",
        "Superheated Header: Blends direct solar steam, flash storage steam, and auxiliary steam."
    ])

    add_card(s4, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.7), "📊 Monitored Sensor Data", [
        "Solar Radiation: Global Horizontal Irradiance (GHI), East DNI, West DNI (W/m²).",
        "Weather Conditions: Ambient Temperature (°C), Wind Speed (km/h).",
        "Hydraulics & Pressure: Feedwater flow rate (t/h), collector pressures (barg), drum temperatures (°C).",
        "Ground Truth Target: High-precision mass flow meter measuring net steam generation (t/h)."
    ])

    s4.notes_slide.notes_text_frame.text = (
        "The dataset comes from an industrial parabolic trough solar thermal plant. It has an East solar field, a West solar field, and 9 high-pressure steam storage tanks. "
        "Every hour, our model ingests solar radiation data—GHI, East and West direct normal irradiance—plus wind speed, ambient temperature, and water pump flows to predict exact steam output."
    )

    # ==========================================
    # SLIDE 5: Data Preprocessing
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Data Engineering", "Dataset Preprocessing & Sensor Fault Resilience", "Ensuring data integrity and 100% operational uptime against hardware dropouts")

    add_card(s5, Inches(0.8), Inches(2.2), Inches(3.6), Inches(4.5), "🌙 1. Night Zero-Clamping", [
        "Sensor drift produces small noise signals at night.",
        "All readings with GHI <= 15 W/m² are clamped to 0.",
        "Prevents unrealistic negative steam flow predictions during non-solar hours."
    ])

    add_card(s5, Inches(4.8), Inches(2.2), Inches(3.6), Inches(4.5), "🛡️ 2. Median Imputation", [
        "Outdoor pyranometers occasionally suffer packet dropouts.",
        "Engineered robust median imputation from training distributions.",
        "Dashboard continues running smoothly without crashing during sensor loss."
    ])

    add_card(s5, Inches(8.8), Inches(2.2), Inches(3.6), Inches(4.5), "📐 3. Geometric Features", [
        "Engineered diurnal cyclic features (hour of day).",
        "Separated East vs. West solar vectors to capture morning vs. afternoon sun incidence.",
        "Evaluated across 359 complete operational calendar days."
    ])

    s5.notes_slide.notes_text_frame.text = (
        "Real factory data is noisy. We handled three major preprocessing steps: First, we filtered out nighttime sensor drift so the model never predicts negative steam. "
        "Second, we built median imputation so if an outdoor sensor drops off the network, the dashboard doesn't crash. "
        "Third, we engineered features for East vs. West fields because morning sun hits the East mirrors while afternoon sun hits the West mirrors."
    )

    # ==========================================
    # SLIDE 6: Model Development
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Deep Learning Architecture", "Seq2Seq 2-Layer LSTM Encoder-Decoder + Bahdanau Attention", "Encoding 48h thermal history to forecast 24h solar steam trajectories")

    add_card(s6, Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7), "🧠 Why Encoder-Decoder Over Tabular ML?", [
        "Thermal Inertia Memory: 2-layer LSTM Encoder (H=64) learns 48h pipe warm-up & cooling dynamics directly.",
        "Bahdanau Attention: Decoder dynamically attends to relevant past hours (e.g. yesterday's peak & recent clouds).",
        "Full 24h Horizon: Predicts all 24 future hours without compounding error from manual lag engineering.",
        "Zero-PyTorch Runtime: 135,073 parameters exported to compressed NumPy with 0.0 t/h parity."
    ])

    add_card(s6, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.7), "🏆 Input Covariates & Attribution", [
        "🥇 GHI (Encoder + Decoder): 46.8% contribution (primary radiative driver).",
        "🥈 Steam History (48h Encoder): 21.4% contribution (thermal momentum).",
        "🥉 West & East DNI: 21.4% combined contribution (directional beam tracking).",
        "🎖️ Cyclic Hour/DOY, Feedwater & Wind: 10.4% diurnal & convective balance."
    ], border_color=TEXT_GREEN)

    s6.notes_slide.notes_text_frame.text = (
        "We upgraded our forecasting core to a 2-Layer LSTM Encoder-Decoder with Bahdanau Attention. "
        "The Encoder reads the past 48 hours of SCADA telemetry into hidden states, and the Decoder autoregressively forecasts the next 24 hours "
        "while attending back to key historical hours. With 135,073 parameters exported to pure NumPy, it runs instantaneously with zero runtime bloat."
    )

    # ==========================================
    # SLIDE 7: Model Performance
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Model Evaluation", "Seq2Seq Model Accuracy & Validation Benchmarks", "Evaluated on 1,729 unseen chronological test windows (41,472 horizon steps)")

    add_stat_box(s7, Inches(0.8), Inches(2.1), Inches(2.7), Inches(2.0), "0.9174", "24h Test R² Score", "91.7% variance explained")
    add_stat_box(s7, Inches(3.8), Inches(2.1), Inches(2.7), Inches(2.0), "1.97 t/h", "24h Test MAE", "Lower than XGBoost (2.08)")
    add_stat_box(s7, Inches(6.8), Inches(2.1), Inches(2.7), Inches(2.0), "0.9808", "Daily R² Score", "Across 359 operational days")
    add_stat_box(s7, Inches(9.8), Inches(2.1), Inches(2.7), Inches(2.0), "+79.0%", "24h Skill Score", "vs. 24h persistence (25.25 t/h)")

    add_card(s7, Inches(0.8), Inches(4.4), Inches(11.7), Inches(2.4), "📈 Key Performance Insights", [
        "Surpasses Legacy XGBoost: Achieves lower 24h MAE (1.973 vs 2.082 t/h) and RMSE (5.295 vs 5.370 t/h).",
        "Multi-Horizon Stability: R² stays > 0.913 and RMSE stays ~5.25 t/h from H+3 all the way through H+24.",
        "Daily Precision: Aggregated daily steam error is 15.19 tons out of 319.93 tons average daily production."
    ])

    s7.notes_slide.notes_text_frame.text = (
        "Evaluated on 41,472 unseen chronological test steps: Our Seq2Seq Encoder-Decoder achieves an R-squared of 0.9174 and MAE of just 1.973 tons per hour, "
        "beating both the 24-hour persistence baseline by +79.03% and our earlier single-step XGBoost baseline."
    )

    # ==========================================
    # SLIDE 8: System Walkthrough
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Operator Experience", "HelioSteam UI & Decision-Support Features", "Built for industrial control rooms with human-in-the-loop AI assistance")

    add_card(s8, Inches(0.8), Inches(2.2), Inches(3.6), Inches(2.3), "📅 1. Multi-Year Selector", [
        "Unlocks 2025, 2026, and 2027 calendar.",
        "1-Click weather profile filters."
    ])
    add_card(s8, Inches(4.8), Inches(2.2), Inches(3.6), Inches(2.3), "📊 2. Three Day-Phases", [
        "Morning Warm-Up (07:00–10:00).",
        "Midday Peak (11:00–15:00).",
        "Evening Stored Steam (16:00–21:00)."
    ])
    add_card(s8, Inches(8.8), Inches(2.2), Inches(3.6), Inches(2.3), "🛢️ 3. Storage Optimization", [
        "Visualizes charging for Tanks 1–9.",
        "Identifies 17-hour zero-LPG windows."
    ])

    add_card(s8, Inches(0.8), Inches(4.8), Inches(5.6), Inches(2.0), "🎮 4. 1-Click Stress Tests & Helio Mascot", [
        "Cloud Ambush, Dusty Mirrors, and Rush Order challenge cards.",
        "Interactive SVG guide 'Helio' walks operators through decisions."
    ], border_color=TEXT_GREEN)

    add_card(s8, Inches(6.8), Inches(4.8), Inches(5.7), Inches(2.0), "🤖 5. Groq Llama-3 AI Advisory", [
        "Live natural-language chatbot tailored to plant engineering.",
        "Gives actionable SCADA valve procedures and safety recommendations."
    ], border_color=TEXT_AMBER)

    s8.notes_slide.notes_text_frame.text = (
        "Now let's look at the live software demo. We designed it in 5 structured steps: Step 1 lets the user pick any date across 2025 to 2027. "
        "Step 2 shows the 24-hour curve split into Morning Warm-up, Midday Peak, and Evening Stored Steam. Step 3 shows thermal storage optimization. "
        "Step 4 features 1-click stress tests like Cloud Ambush, guided by our character mascot Helio. And Step 5 integrates live Groq Llama-3 AI chat for operator support."
    )

    # ==========================================
    # SLIDE 9: Economic & Carbon ROI
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Industrial Impact", "Measurable Economic & Environmental Returns", "Demonstrated on a typical summer peak generation day (July 16)")

    add_stat_box(s9, Inches(0.8), Inches(2.1), Inches(2.7), Inches(2.1), "945.4 t", "Solar Steam Made", "Clean high-pressure output")
    add_stat_box(s9, Inches(3.8), Inches(2.1), Inches(2.7), Inches(2.1), "24,966 kg", "LPG Fuel Saved", "Displaced in one sunny day")
    add_stat_box(s9, Inches(6.8), Inches(2.1), Inches(2.7), Inches(2.1), "$22,969", "Daily Cost Savings", "> $1.2M USD annually")
    add_stat_box(s9, Inches(9.8), Inches(2.1), Inches(2.7), Inches(2.1), "74.9 t", "CO2 Avoided", "Carbon emissions stopped")

    add_card(s9, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.3), "🌟 Peak Operational Milestone: 17 Hours of Zero LPG", [
        "By charging Tanks 1–9 during peak solar surplus (11:00–16:00), stored thermal energy carries the evening shift.",
        "The fossil fuel boiler is 100% turned OFF from 06:00 to 23:00 CET without any risk of factory downtime.",
        "Saves 42.0 kg/h in auxiliary standby burner losses while preventing thermal shocks."
    ], border_color=TEXT_GREEN)

    s9.notes_slide.notes_text_frame.text = (
        "What does this mean in real business numbers? On a typical sunny day, our system manages 945 tons of solar steam. "
        "That saves nearly 25,000 kilograms of LPG, saves $22,969 dollars in a single day, and prevents 74.9 tons of CO2 from entering our atmosphere. "
        "That is equivalent to over 1.2 million dollars saved per year."
    )

    # ==========================================
    # SLIDE 10: Conclusion
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)

    tbox10 = s10.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.33), Inches(4.0))
    tf10 = tbox10.text_frame
    tf10.word_wrap = True

    p_badge10 = tf10.paragraphs[0]
    p_badge10.text = "✓ PROJECT CONCLUSION & TAKEAWAY"
    p_badge10.alignment = PP_ALIGN.CENTER
    p_badge10.font.size = Pt(12)
    p_badge10.font.bold = True
    p_badge10.font.color.rgb = TEXT_GREEN
    p_badge10.space_after = Pt(16)

    p_hero10 = tf10.add_paragraph()
    p_hero10.text = "Turning Unpredictable Sunlight into Dependable Industrial Power"
    p_hero10.alignment = PP_ALIGN.CENTER
    p_hero10.font.size = Pt(32)
    p_hero10.font.bold = True
    p_hero10.font.color.rgb = TEXT_WHITE
    p_hero10.space_after = Pt(14)

    p_sub10 = tf10.add_paragraph()
    p_sub10.text = "Decarbonizing industrial heat does not just require solar hardware—it requires smart predictive software. HelioSteam proves that machine learning makes renewable steam reliable, cost-effective, and safe."
    p_sub10.alignment = PP_ALIGN.CENTER
    p_sub10.font.size = Pt(15)
    p_sub10.font.color.rgb = TEXT_MUTED
    p_sub10.space_after = Pt(28)

    p_thanks = tf10.add_paragraph()
    p_thanks.text = "Thank You! — Ready for Questions & Discussion"
    p_thanks.alignment = PP_ALIGN.CENTER
    p_thanks.font.size = Pt(18)
    p_thanks.font.bold = True
    p_thanks.font.color.rgb = TEXT_AMBER

    s10.notes_slide.notes_text_frame.text = (
        "In conclusion: Transitioning heavy manufacturing away from fossil fuels doesn't just require solar hardware—it requires smart predictive software. "
        "By bridging industrial SCADA telemetry with machine learning forecasting and generative AI decision support, HelioSteam transforms unpredictable solar energy into a dependable, cost-saving, and zero-emission industrial power source. "
        "Thank you, and I am now ready for your questions."
    )

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HelioSteam_AI_Presentation.pptx")
    prs.save(out_path)
    print(f"Presentation successfully created at: {out_path}")

if __name__ == "__main__":
    create_presentation()
