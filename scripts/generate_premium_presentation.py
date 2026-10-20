import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def add_slide_transition(slide, trans_type="fade"):
    """Adds native PowerPoint transition XML to a slide."""
    if trans_type == "push":
        xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:push dir="r"/></p:transition>'
    elif trans_type == "wipe":
        xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:wipe dir="r"/></p:transition>'
    else: # fade
        xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p:fade/></p:transition>'
    slide._element.append(parse_xml(xml))

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Visual Theme - Executive Tech Slate & Glowing Neon Accents
    C_BG = RGBColor(7, 17, 30)          # #07111E - Deep Canvas
    C_CARD = RGBColor(14, 33, 56)       # #0E2138 - Card Surface
    C_CARD_ALT = RGBColor(18, 42, 70)   # #122A46 - Highlight Card
    C_BORDER = RGBColor(30, 58, 95)     # #1E3A5F - Subtle Edge
    C_CYAN = RGBColor(0, 229, 255)      # #00E5FF - Vibrant Electric Cyan
    C_TEAL = RGBColor(0, 180, 216)      # #00B4D8 - Secondary Accent
    C_GOLD = RGBColor(255, 183, 3)      # #FFB703 - Warm Amber Gold
    C_WHITE = RGBColor(255, 255, 255)   # Crisp White
    C_MUTED = RGBColor(160, 178, 201)   # #A0B2C9 - Neutral Slate Text
    C_GREEN = RGBColor(0, 230, 118)     # #00E676 - Success Metric Green

    def fill_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.color.rgb = C_BG
        return bg

    def add_top_bar(slide, title, category="OPERATING SYSTEMS / AI PROJECT PRESENTATION • REVIEW 1 & 2"):
        # Header Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN
        p_cat.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Glowing accent rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.04))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_CYAN
        rule.line.color.rgb = C_CYAN

    def add_glow_card(slide, left, top, width, height, title="", pill_tag="", bg=C_CARD, border=C_BORDER, accent_color=C_CYAN):
        # Card body
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1.2)

        # Top accent highlight stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.2), top, width - Inches(0.4), Inches(0.04))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = accent_color
        stripe.line.color.rgb = accent_color

        tf = card.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.28)
        tf.margin_right = Inches(0.28)
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.2)
        tf.word_wrap = True

        if pill_tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = pill_tag.upper()
            p_tag.font.size = Pt(8.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = accent_color
            p_tag.space_after = Pt(3)

        if title:
            p_title = tf.add_paragraph() if pill_tag else tf.paragraphs[0]
            p_title.text = title
            p_title.font.size = Pt(13)
            p_title.font.bold = True
            p_title.font.color.rgb = C_WHITE
            p_title.space_after = Pt(8)

        return card, tf

    def add_bullet(tf, bold_prefix, text, size=10, space_after=5, color=C_MUTED, bold_color=C_CYAN):
        p = tf.add_paragraph()
        p.space_after = Pt(space_after)
        
        r1 = p.add_run()
        r1.text = "▸ " + bold_prefix + " "
        r1.font.bold = True
        r1.font.size = Pt(size)
        r1.font.color.rgb = bold_color

        r2 = p.add_run()
        r2.text = text
        r2.font.bold = False
        r2.font.size = Pt(size)
        r2.font.color.rgb = color

    # =========================================================================
    # SLIDE 1: ULTRA-PREMIUM TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    fill_bg(s1)
    add_slide_transition(s1, "fade")

    # Glowing decorative elements
    pill_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.85), Inches(4.8), Inches(0.42))
    pill_badge.fill.solid()
    pill_badge.fill.fore_color.rgb = RGBColor(16, 40, 72)
    pill_badge.line.color.rgb = C_CYAN
    pill_badge.line.width = Pt(1)
    p_b = pill_badge.text_frame.paragraphs[0]
    p_b.text = "LAB COMPONENT EVALUATION • TOTAL MARKS: 30"
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = C_CYAN
    p_b.alignment = PP_ALIGN.CENTER

    # Main Project Title Box
    tbox = s1.shapes.add_textbox(Inches(0.9), Inches(1.4), Inches(11.5), Inches(2.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "Repository-Aware AI Software Engineering Copilot"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Hierarchical AST Parsing, Call-Graph Dependency Analysis, and Hybrid Retrieval for Large-Scale Codebases"
    p2.font.size = Pt(15.5)
    p2.font.italic = True
    p2.font.color.rgb = C_MUTED
    p2.space_after = Pt(12)

    # 4 Quick Metric Badges in Title Slide
    kpi_data = [
        ("94.3%", "P@5 Retrieval Precision", C_CYAN),
        ("0.912", "MRR@10 Ranking Accuracy", C_GOLD),
        ("560 ms", "Average TTFT Latency", C_GREEN),
        ("100%", "Local Privacy / 0 Cloud Leak", C_TEAL)
    ]
    for idx, (num, lbl, col) in enumerate(kpi_data):
        kpi_x = Inches(0.9 + idx * 2.9)
        k_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kpi_x, Inches(3.2), Inches(2.7), Inches(1.15))
        k_card.fill.solid()
        k_card.fill.fore_color.rgb = C_CARD
        k_card.line.color.rgb = C_BORDER
        tf_k = k_card.text_frame
        tf_k.margin_top = Inches(0.12)
        p_num = tf_k.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(18)
        p_num.font.bold = True
        p_num.font.color.rgb = col
        p_num.alignment = PP_ALIGN.CENTER
        p_lbl = tf_k.add_paragraph()
        p_lbl.text = lbl
        p_lbl.font.size = Pt(8.5)
        p_lbl.font.color.rgb = C_MUTED
        p_lbl.alignment = PP_ALIGN.CENTER

    # Student Cards Bottom Left
    s_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.7), Inches(5.6), Inches(2.1))
    s_card.fill.solid()
    s_card.fill.fore_color.rgb = C_CARD
    s_card.line.color.rgb = C_CYAN
    s_card.line.width = Pt(1.5)
    tf_s = s_card.text_frame
    tf_s.margin_left = Inches(0.3)
    tf_s.margin_top = Inches(0.2)

    p_stitle = tf_s.paragraphs[0]
    p_stitle.text = "PROJECT AUTHORS & RESEARCHERS"
    p_stitle.font.size = Pt(10)
    p_stitle.font.bold = True
    p_stitle.font.color.rgb = C_GOLD
    p_stitle.space_after = Pt(8)

    p_s1 = tf_s.add_paragraph()
    p_s1.text = "1. Mogalapalli Sohan"
    p_s1.font.size = Pt(14)
    p_s1.font.bold = True
    p_s1.font.color.rgb = C_WHITE
    p_s1_sub = tf_s.add_paragraph()
    p_s1_sub.text = "    Reg No: 24BCE2625 | Lead Architect & ML Pipeline"
    p_s1_sub.font.size = Pt(9.5)
    p_s1_sub.font.color.rgb = C_CYAN
    p_s1_sub.space_after = Pt(6)

    p_s2 = tf_s.add_paragraph()
    p_s2.text = "2. Mogalapalli Rohan"
    p_s2.font.size = Pt(14)
    p_s2.font.bold = True
    p_s2.font.color.rgb = C_WHITE
    p_s2_sub = tf_s.add_paragraph()
    p_s2_sub.text = "    Reg No: 24BCE2622 | Graph Analytics & Backend Core"
    p_s2_sub.font.size = Pt(9.5)
    p_s2_sub.font.color.rgb = C_CYAN

    # Department & Affiliation Card Right
    a_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.7), Inches(5.6), Inches(2.1))
    a_card.fill.solid()
    a_card.fill.fore_color.rgb = C_CARD
    a_card.line.color.rgb = C_BORDER
    tf_a = a_card.text_frame
    tf_a.margin_left = Inches(0.3)
    tf_a.margin_top = Inches(0.2)

    p_atitle = tf_a.paragraphs[0]
    p_atitle.text = "ACADEMIC INSTITUTION"
    p_atitle.font.size = Pt(10)
    p_atitle.font.bold = True
    p_atitle.font.color.rgb = C_TEAL
    p_atitle.space_after = Pt(8)

    p_dept = tf_a.add_paragraph()
    p_dept.text = "Department of Computer Science and Engineering"
    p_dept.font.size = Pt(13)
    p_dept.font.bold = True
    p_dept.font.color.rgb = C_WHITE
    p_dept.space_after = Pt(2)

    p_school = tf_a.add_paragraph()
    p_school.text = "School of Computer Science and Engineering"
    p_school.font.size = Pt(11)
    p_school.font.color.rgb = C_MUTED
    p_school.space_after = Pt(8)

    p_eval = tf_a.add_paragraph()
    p_eval.text = "Review 1 & 2 Combined Comprehensive Submission"
    p_eval.font.size = Pt(10)
    p_eval.font.bold = True
    p_eval.font.color.rgb = C_GOLD

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & AT-A-GLANCE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    fill_bg(s2)
    add_top_bar(s2, "Executive Summary & System Overview", "System At-A-Glance")
    add_slide_transition(s2, "push")

    summary_cards = [
        ("The Challenge", "CONTEXT & GRAPH BLINDNESS", 
         [("Cognitive Load: ", "Developers spend up to 58% of their time reading and tracing code rather than writing features [1], [2]."),
          ("Scope Severance: ", "Standard LLM chunkers cut functions arbitrarily, losing class headers and imports [11]."),
          ("Identifier Blindness: ", "Dense vectors confuse similar tokens (getUserById vs getUsersById) [12], [23]."),
          ("Privacy Risks: ", "Cloud copilots leak private IP across public networks [15].")],
         Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), C_CYAN),

        ("The Solution", "AST + GRAPH + HYBRID RAG",
         [("Tree-sitter AST: ", "Extracts concrete syntax across 8 programming languages deterministically [11]."),
          ("Breadcrumb Scope: ", "Prepends file, class, decorator, and import breadcrumbs into every chunk."),
          ("Tri-Modal RRF: ", "Blends FAISS dense search, BM25 Okapi lexical index, and exact symbol boost [20]."),
          ("Directed Graph: ", "NetworkX computes multi-hop blast radiuses & PageRank architectural hubs [14], [22].")],
         Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4), C_GOLD),

        ("The Outcomes", "VALIDATED RESULTS & PRIVACY",
         [("Precision Boost: ", "Achieves 94.3% top-5 retrieval precision and 0.912 MRR@10 (vs 0.724 dense)."),
          ("Rapid Response: ", "Streams first response token in ~310 ms with full answer in ~560 ms on local GPU."),
          ("100% Grounded: ", "Strict file:start-end citations eliminate API hallucinations completely [7], [10]."),
          ("Air-Gapped: ", "Runs locally via Ollama (Qwen2.5-Coder:7b) without sending any code off-premise.")],
         Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4), C_GREEN)
    ]

    for title, pill, bullets, l, t, w, h, col in summary_cards:
        _, tf_sc = add_glow_card(s2, l, t, w, h, title, pill, accent_color=col)
        for b_pre, b_text in bullets:
            add_bullet(tf_sc, b_pre, b_text, size=9.5, space_after=8, bold_color=col)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    fill_bg(s3)
    add_top_bar(s3, "Problem Formulation & Empirical Motivation", "Component 1: Problem & Motivation")
    add_slide_transition(s3, "push")

    _, tf3_1 = add_glow_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Software Engineering Reality", "THE INDUSTRIAL MOTIVATION", accent_color=C_GOLD)
    add_bullet(tf3_1, "Maintenance Overhead: ", "Studies across IEEE/ACM show software comprehension consumes >50% of developer effort in enterprise teams [1], [2].", 10, 8, bold_color=C_GOLD)
    add_bullet(tf3_1, "Monolithic Repositories: ", "Enterprise codebases span 100k+ LOC, hundreds of microservices, and asynchronous contracts that cannot fit into standard LLM contexts [3].", 10, 8, bold_color=C_GOLD)
    add_bullet(tf3_1, "High Regression Costs: ", "Localized code edits trigger downstream breaking changes across unseen caller chains without static dependency safety [4], [17].", 10, 8, bold_color=C_GOLD)
    add_bullet(tf3_1, "Security & Compliance: ", "Air-gapped finance, healthcare, and enterprise firms strictly prohibit cloud-based code telemetry [15].", 10, 8, bold_color=C_GOLD)

    _, tf3_2 = add_glow_card(s3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "5 Critical Failure Modes of Existing Tools", "THE ACADEMIC PROBLEM", accent_color=C_CYAN)
    add_bullet(tf3_2, "1. Context Window Saturation: ", "Raw context stuffing suffers from 'lost-in-the-middle' attention collapse and cost bottlenecks [10].", 10, 7)
    add_bullet(tf3_2, "2. Syntactic Scope Severance: ", "Naive line splitters bisect methods mid-block, severing enclosing class headers, decorators, and imports [11].", 10, 7)
    add_bullet(tf3_2, "3. Identifier Blindness in Vector Search: ", "Dense neural encoders fail to distinguish subtle variable tokens (e.g., getUserById vs getUsersById) [12], [23].", 10, 7)
    add_bullet(tf3_2, "4. Call-Graph & Dependency Blindness: ", "Vector stores treat code as flat natural language, ignoring caller-callee chains and circular dependencies [14], [22].", 10, 7)
    add_bullet(tf3_2, "5. Hallucinated Non-Existent APIs: ", "LLMs invent plausible but non-existent APIs without verifiable line citations.")

    # =========================================================================
    # SLIDE 4: PROJECT OBJECTIVES
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    fill_bg(s4)
    add_top_bar(s4, "Technical Project Objectives", "Component 1: Target Objectives & Scope")
    add_slide_transition(s4, "push")

    objs = [
        ("1. Multi-Language AST Parsing", "STATIC PARSING",
         "Construct native Tree-sitter parsers supporting 8 programming languages (Python, TypeScript, JS, Java, C++, C, Go, Rust) to extract concrete syntax trees, functions, classes, imports, and calls [11].",
         Inches(0.8), Inches(1.5), C_CYAN),

        ("2. Breadcrumb Scope Chunking", "SEMANTIC CHUNKING",
         "Eliminate orphan code chunks by recursively traversing the AST to inject hierarchical header breadcrumbs (# File, # Class Scope, # Decorators, # Imports) before vector embedding.",
         Inches(6.8), Inches(1.5), C_TEAL),

        ("3. Tri-Modal Hybrid Retrieval", "RANK FUSION (RRF)",
         "Implement Reciprocal Rank Fusion (RRF) unifying FAISS dense vectors (nomic-embed), BM25 Okapi lexical inverted index, and exact AST symbol boosting [20], [21].",
         Inches(0.8), Inches(4.3), C_GOLD),

        ("4. Program Graph Blast Radius", "DEPENDENCY ANALYTICS",
         "Construct directed program graphs via NetworkX to compute module PageRank hubs, circular dependency cycles, and predict multi-hop change impact risk tiers [14], [17], [22].",
         Inches(6.8), Inches(4.3), C_GREEN)
    ]

    for title, pill, desc, l, t, col in objs:
        _, tf_obj = add_glow_card(s4, l, t, Inches(5.7), Inches(2.55), title, pill, accent_color=col)
        p = tf_obj.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 5: EXISTING SYSTEMS VS PROPOSED
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    fill_bg(s5)
    add_top_bar(s5, "Comparative Analysis: Existing Systems vs. Our Approach", "Component 1: Existing Systems & Approaches")
    add_slide_transition(s5, "push")

    t5_shape = s5.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.3))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(2.2)
    t5.columns[1].width = Inches(2.2)
    t5.columns[2].width = Inches(2.3)
    t5.columns[3].width = Inches(2.4)
    t5.columns[4].width = Inches(2.633)

    t5_headers = ["Key Dimension", "Ripgrep / Ctags", "Naive RAG (LangChain)", "Cloud Copilot (GitHub)", "Proposed Copilot (Our Work)"]
    for i, h in enumerate(t5_headers):
        cell = t5.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_CYAN if i == 4 else C_WHITE
        p.alignment = PP_ALIGN.CENTER

    t5_rows = [
        ("Chunking Strategy", "Regex token lines", "Fixed token/character window", "Active file editor buffer", "AST Breadcrumb Scope Enriched"),
        ("Retrieval Engine", "Lexical Pattern Match", "Dense Vector Only", "Proprietary Cloud Heuristics", "Tri-Modal Hybrid (Dense+BM25+Symbol RRF)"),
        ("Call Graph & Impact", "None", "None (Flat text)", "Limited single-file hops", "NetworkX Directed Graph + Blast Radius Tiers"),
        ("Privacy & Execution", "100% Local (CLI)", "Cloud API (OpenAI/Anthropic)", "Cloud Third-Party Servers", "100% Local Inference (Ollama Qwen2.5-Coder)")
    ]

    for row_idx, data in enumerate(t5_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t5.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD if row_idx % 2 == 1 else RGBColor(11, 26, 46)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_GOLD
            elif col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_GREEN
            else:
                p.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 6: LITERATURE SURVEY MATRIX
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    fill_bg(s6)
    add_top_bar(s6, "Literature Survey & Theoretical Foundations", "Component 1: Literature Survey (Google Scholar)")
    add_slide_transition(s6, "push")

    t6_shape = s6.shapes.add_table(6, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.3))
    t6 = t6_shape.table
    t6.columns[0].width = Inches(2.2)
    t6.columns[1].width = Inches(3.6)
    t6.columns[2].width = Inches(2.9)
    t6.columns[3].width = Inches(3.033)

    t6_headers = ["Author & Venue", "Core Methodology & Contribution", "Key Strength", "Identified Research Limitation"]
    for i, h in enumerate(t6_headers):
        cell = t6.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_CYAN if i == 0 else C_WHITE
        p.alignment = PP_ALIGN.CENTER

    t6_rows = [
        ("Ferrante et al. [14]\nACM TOPLAS", "Program Dependence Graphs (PDG) for control & data flow modeling", "Formal reachability and program slicing guarantees", "Pure compiler optimization; no neural or vector search."),
        ("Kramer [11]\nACM SPLASH", "Incremental Tree-sitter parsing for multi-language software syntax trees", "Sub-millisecond AST updates across edits", "Parses syntax only; no semantic retrieval or LLM reasoning."),
        ("Gu et al. [12]\nIEEE/ACM ICSE", "Deep Code Search (DeepCS) using dual-encoder neural representations", "Learns high-level semantic developer intent", "Poor precision on exact identifier tokens and method definitions."),
        ("Robertson et al. [21]\nFoundations in IR", "Probabilistic BM25 Okapi lexical term frequency ranking framework", "Unmatched deterministic exact-token accuracy", "Completely fails on natural language synonyms and concepts."),
        ("Zhang et al. [3]\nEMNLP", "RepoCoder: Iterative retrieval-augmented generation for repositories", "Improves cross-file completion via sliding windows", "Lacks AST breadcrumb scope headers and call-graph blast analysis.")
    ]

    for row_idx, data in enumerate(t6_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t6.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD if row_idx % 2 == 1 else RGBColor(11, 26, 46)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_GOLD
            else:
                p.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 7: PATENT PRIOR-ART MATRIX
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    fill_bg(s7)
    add_top_bar(s7, "Patent Prior-Art Analysis (Google Patents)", "Component 1: Patent-Track Evaluation")
    add_slide_transition(s7, "push")

    t7_shape = s7.shapes.add_table(6, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.2))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(2.0)
    t7.columns[1].width = Inches(1.8)
    t7.columns[2].width = Inches(3.9)
    t7.columns[3].width = Inches(4.033)

    t7_headers = ["Patent / Pub. No.", "Assignee (Year)", "Disclosed Invention Description", "Key Differentiation in Our System"]
    for i, h in enumerate(t7_headers):
        cell = t7.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_CYAN if i == 0 else C_WHITE
        p.alignment = PP_ALIGN.CENTER

    t7_rows = [
        ("US11,288,046 B2 [25]", "Microsoft (2022)", "Synthesizing code using neural networks and local file context", "Relies on flat text buffers; lacks AST breadcrumb metadata injection into embeddings."),
        ("US11,768,918 B1 [26]", "Amazon (2023)", "Code completion using language models conditioned on repository metadata", "Targets token autocompletion; does not build directed call graphs for blast radius risk estimation."),
        ("US2023/0385367 A1 [27]", "Google LLC (2023)", "Semantic code search using dual-encoder vector embeddings", "Dense-only; lacks hybrid Reciprocal Rank Fusion with exact AST symbol boost."),
        ("US10,846,063 B2 [28]", "IBM Corp (2020)", "Static dependency analysis for microservice impact assessment", "Pure static rule analysis; lacks generative RAG reasoning and interactive natural language QA."),
        ("US11,487,516 B1 [29]", "Meta (2022)", "Automated change analysis utilizing call graph traversal", "Focuses on build failure regression; does not integrate local LLM prompt grounding or breadcrumbs.")
    ]

    for row_idx, data in enumerate(t7_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t7.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD if row_idx % 2 == 1 else RGBColor(11, 26, 46)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_GOLD
            else:
                p.font.color.rgb = C_MUTED

    _, tf_cl = add_glow_card(s7, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.2), "Potentially Protectable Novel Claims (Invention Disclosures)", "INVENTION CLAIMS", accent_color=C_GOLD)
    add_bullet(tf_cl, "Claim 1: ", "Context-Enriched Breadcrumb Chunk Injection: Recursively prepending AST scopes into vector embedding payloads.", 9.5, 2, bold_color=C_GOLD)
    add_bullet(tf_cl, "Claim 2: ", "Tri-Modal Reciprocal Rank Fusion: Fusing dense vectors, lexical BM25, and exact AST symbol matches with calibrated code weights.", 9.5, 2, bold_color=C_GOLD)
    add_bullet(tf_cl, "Claim 3: ", "Graph-Augmented Blast-Radius Impact Grounding: Mapping directed call reachability to risk tiers for predictive LLM reasoning.", 9.5, 2, bold_color=C_GOLD)

    # =========================================================================
    # SLIDE 8: SYSTEM ARCHITECTURE
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    fill_bg(s8)
    add_top_bar(s8, "End-to-End Holistic System Architecture", "Component 2: System Architecture & Workflow")
    add_slide_transition(s8, "push")

    img_path = "architecture_diagram.png"
    if os.path.exists(img_path):
        s8.shapes.add_picture(img_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.6))

    _, tf8 = add_glow_card(s8, Inches(9.0), Inches(1.5), Inches(3.533), Inches(5.6), "Pipeline Modules", "SYSTEM COMPONENTS", accent_color=C_CYAN)
    add_bullet(tf8, "1. Ingestion Engine: ", "Scans repo files honoring .gitignore & language rules.", 10, 8)
    add_bullet(tf8, "2. AST Extractor: ", "Tree-sitter concrete syntax trees across 8 languages [11].", 10, 8)
    add_bullet(tf8, "3. Breadcrumb Chunker: ", "Injects parent class, imports & decorators into snippets.", 10, 8)
    add_bullet(tf8, "4. Program Graph: ", "NetworkX computes PageRank hubs & call chains [14], [22].", 10, 8)
    add_bullet(tf8, "5. Dual-Index Search: ", "FAISS (nomic-embed) + BM25 Okapi with identifier splitters.", 10, 8)
    add_bullet(tf8, "6. Dual Reasoner: ", "Streaming RAG with line citations + ReAct Agent [7], [10].", 10, 8)

    # =========================================================================
    # SLIDE 9: ALGORITHMS & FORMULATIONS
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    fill_bg(s9)
    add_top_bar(s9, "Algorithms & Mathematical Formulations", "Component 2: Mathematical Foundations")
    add_slide_transition(s9, "push")

    _, tf9_1 = add_glow_card(s9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Tri-Modal Reciprocal Rank Fusion", "ALGORITHM 1: RANK FUSION", accent_color=C_CYAN)
    add_bullet(tf9_1, "Problem Addressed: ", "Direct score averaging fails because cosine similarities and BM25 scores operate on entirely different scales [20].")
    
    p_box1 = tf9_1.add_paragraph()
    p_box1.text = "Score_RRF(d) = \n  [ w_dense / (k + rank_dense(d)) ]\n+ [ w_bm25 / (k + rank_bm25(d)) ]\n+ [ w_sym / (k + rank_sym(d)) ]"
    p_box1.font.bold = True
    p_box1.font.size = Pt(13)
    p_box1.font.color.rgb = C_CYAN
    p_box1.space_after = Pt(10)

    add_bullet(tf9_1, "Smoothing Constant: ", "k = 60 prevents disproportionate penalties for high-rank entries.")
    add_bullet(tf9_1, "Empirical Weighting: ", "w_dense = 1.0 (intent), w_bm25 = 0.8 (tokens), w_sym = 1.2 (symbol boost).")
    add_bullet(tf9_1, "Deterministic Boost: ", "Guarantees exact function definitions rise to rank-1 instantly.")

    _, tf9_2 = add_glow_card(s9, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Graph Blast-Radius & Impact Assessment", "ALGORITHM 2: GRAPH IMPACT", accent_color=C_GOLD)
    add_bullet(tf9_2, "Reachability Formulation: ", "Let G = (V, E) be the directed dependency graph [14], [22].", bold_color=C_GOLD)

    p_box2 = tf9_2.add_paragraph()
    p_box2.text = "Impact(s, D) = \n{ v in V | exists path s ->* v with length <= D }"
    p_box2.font.bold = True
    p_box2.font.size = Pt(13)
    p_box2.font.color.rgb = C_GOLD
    p_box2.space_after = Pt(10)

    add_bullet(tf9_2, "Risk Tier Classification [17], [18]:", "", bold_color=C_GOLD)
    add_bullet(tf9_2, "CRITICAL: ", "|Impact| >= 15 or symbol in top 5% PageRank.", bold_color=RGBColor(255, 82, 82))
    add_bullet(tf9_2, "HIGH: ", "8 <= |Impact| < 15 downstream modules.", bold_color=RGBColor(255, 145, 0))
    add_bullet(tf9_2, "MEDIUM: ", "3 <= |Impact| < 8 downstream modules.", bold_color=C_GOLD)
    add_bullet(tf9_2, "LOW: ", "|Impact| < 3 (strictly isolated changes).", bold_color=C_GREEN)

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL BENCHMARKS
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    fill_bg(s10)
    add_top_bar(s10, "Experimental Results & Validation Benchmarks", "Component 3: Implementation & Validation")
    add_slide_transition(s10, "push")

    t10_shape = s10.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(6.8), Inches(3.6))
    t10_t = t10_shape.table
    t10_t.columns[0].width = Inches(2.4)
    t10_t.columns[1].width = Inches(1.1)
    t10_t.columns[2].width = Inches(1.1)
    t10_t.columns[3].width = Inches(1.1)
    t10_t.columns[4].width = Inches(1.1)

    t10_headers = ["Retrieval Strategy", "P@1 (%)", "P@5 (%)", "R@5 (%)", "MRR@10"]
    for i, h in enumerate(t10_headers):
        cell = t10_t.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_CYAN if i == 4 else C_WHITE
        p.alignment = PP_ALIGN.CENTER

    t10_rows = [
        ("Dense Vector Only (FAISS)", "68.4", "74.2", "71.5", "0.724"),
        ("Lexical Only (BM25)", "61.2", "69.8", "66.2", "0.658"),
        ("Hybrid (Simple Average)", "76.5", "82.1", "79.4", "0.789"),
        ("Proposed Hybrid (RRF)", "89.7", "94.3", "92.8", "0.912")
    ]

    for row_idx, data in enumerate(t10_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t10_t.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(16, 44, 76) if row_idx == 4 else (C_CARD if row_idx % 2 == 1 else RGBColor(11, 26, 46))
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if row_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_GREEN if col_idx > 0 else C_WHITE
            else:
                p.font.color.rgb = C_MUTED
            if col_idx > 0:
                p.alignment = PP_ALIGN.CENTER

    t10_lat = s10.shapes.add_table(7, 3, Inches(7.9), Inches(1.5), Inches(4.6), Inches(3.6))
    t10_l = t10_lat.table
    t10_l.columns[0].width = Inches(2.2)
    t10_l.columns[1].width = Inches(1.3)
    t10_l.columns[2].width = Inches(1.1)

    t10_l_headers = ["Pipeline Stage", "Mechanism", "Latency"]
    for i, h in enumerate(t10_l_headers):
        cell = t10_l.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_CYAN if i == 2 else C_WHITE
        p.alignment = PP_ALIGN.CENTER

    t10_l_rows = [
        ("AST Entity Parsing", "Tree-sitter", "42 ms / 1k"),
        ("Embedding Gen (x10)", "nomic-embed", "185 ms"),
        ("Dual-Index Search", "FAISS + BM25", "18 ms"),
        ("Blast Radius BFS", "NetworkX", "6 ms"),
        ("Time to First Token", "Ollama Qwen2.5", "310 ms"),
        ("Cumulative Response", "Streaming RAG", "~560 ms")
    ]

    for row_idx, data in enumerate(t10_l_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t10_l.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(16, 44, 76) if row_idx == 6 else (C_CARD if row_idx % 2 == 1 else RGBColor(11, 26, 46))
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            if row_idx == 6:
                p.font.bold = True
                p.font.color.rgb = C_GREEN if col_idx > 0 else C_WHITE
            else:
                p.font.color.rgb = C_MUTED
            if col_idx > 0:
                p.alignment = PP_ALIGN.CENTER

    _, tf10_b = add_glow_card(s10, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.7), "Empirical Validation Summary", "KEY TAKEAWAYS", accent_color=C_GREEN)
    add_bullet(tf10_b, "Precision Superiority: ", "Tri-Modal RRF achieves 0.912 MRR@10, significantly outperforming standalone vector (0.724) and BM25 (0.658).", 10, 3, bold_color=C_GREEN)
    add_bullet(tf10_b, "Low Interactive Latency: ", "First token streams in ~310 ms; complete grounded response delivered in ~560 ms on standard developer workstation.", 10, 3, bold_color=C_GREEN)
    add_bullet(tf10_b, "Zero Citational Hallucination: ", "Enriched breadcrumb chunks allow Qwen2.5-Coder to ground 100% of generated responses in exact repository line numbers.", 10, 3, bold_color=C_GREEN)

    # =========================================================================
    # SLIDE 11: RUBRIC COMPLIANCE (30 MARKS)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    fill_bg(s11)
    add_top_bar(s11, "Review 1 & 2 Rubric Compliance Mapping (Marks: 30)", "Evaluation Rubric Alignment")
    add_slide_transition(s11, "push")

    t11_shape = s11.shapes.add_table(4, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.3))
    t11 = t11_shape.table
    t11.columns[0].width = Inches(2.2)
    t11.columns[1].width = Inches(3.1)
    t11.columns[2].width = Inches(3.2)
    t11.columns[3].width = Inches(3.233)

    t11_headers = ["Rubric Component", "Common Deliverables", "Conference Paper Track", "Patent Track Deliverables"]
    for i, h in enumerate(t11_headers):
        cell = t11.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_CYAN if i == 0 else C_WHITE
        p.alignment = PP_ALIGN.CENTER

    t11_rows = [
        ("Component 1:\nProblem & Literature\n(Review 1 - 10 Marks)", "Title, Problem Statement, Motivation, Objectives, Existing System, Literature Survey, Research Gap.", "Survey of 24 Google Scholar papers [1]–[24], analytical comparison, and contribution claims.", "Prior-art study of 5 Google Patents [25]–[29], novelty identification, protectable claims."),
        ("Component 2:\nProposed Methodology\n(Review 2)", "Proposed Architecture (Fig. 1), workflow, modules, algorithms, technologies.", "AST breadcrumb method, Tri-Modal RRF (Eq. 1), and NetworkX call graph blast radius (Eq. 2).", "Detailed invention architecture, novel mechanism description, and protectable claims 1–3."),
        ("Component 3:\nValidation & Prototype", "Implementation status, screenshots, experimental setup, latency profile.", "Benchmark evaluation, baseline comparison (Table III), precision/recall metrics.", "Working local prototype demonstration and empirical validation evidence.")
    ]

    for row_idx, data in enumerate(t11_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t11.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD if row_idx % 2 == 1 else RGBColor(11, 26, 46)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_GOLD
            else:
                p.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    fill_bg(s12)
    add_top_bar(s12, "Conclusion & Future Research Directions", "Project Summary & Outlook")
    add_slide_transition(s12, "fade")

    _, tf12_1 = add_glow_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Core Project Accomplishments", "KEY ACHIEVEMENTS", accent_color=C_CYAN)
    add_bullet(tf12_1, "Deterministic Grounding: ", "Coupled Tree-sitter ASTs with breadcrumb injection to achieve 94.3% top-5 retrieval precision [11].", 10, 8)
    add_bullet(tf12_1, "High-Precision Ranking: ", "Tri-Modal RRF achieves 0.912 MRR@10, resolving the dense-sparse code search trade-off [20].", 10, 8)
    add_bullet(tf12_1, "Change Blast Radius: ", "NetworkX directed graph evaluates multi-hop ripple effects and categorizes risk tiers [14], [22].", 10, 8)
    add_bullet(tf12_1, "100% Local Privacy: ", "Air-gapped execution via Ollama (Qwen2.5-Coder:7b) with zero third-party cloud data leakage.", 10, 8)

    _, tf12_2 = add_glow_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Future Research Directions", "FUTURE SCOPE", accent_color=C_GOLD)
    add_bullet(tf12_2, "Dynamic Runtime Profiling: ", "Integrate eBPF and runtime telemetry to merge static call graphs with dynamic execution traces.", 10, 8, bold_color=C_GOLD)
    add_bullet(tf12_2, "Automated Test Synthesis: ", "Leverage blast-radius impact sets to automatically synthesize regression unit tests [24].", 10, 8, bold_color=C_GOLD)
    add_bullet(tf12_2, "Multi-Agent Code Repair: ", "Deploy cooperative agent teams for automated multi-file code repairs and pull requests.", 10, 8, bold_color=C_GOLD)
    add_bullet(tf12_2, "IDE Extension Ecosystem: ", "Package the backend into lightweight VS Code and JetBrains LSP sidecars.", 10, 8, bold_color=C_GOLD)

    out_file = "AI_Software_Engineering_Copilot_Pro_Presentation.pptx"
    prs.save(out_file)
    print(f"Ultra-polished presentation saved to: {out_file}")

if __name__ == "__main__":
    build_presentation()
