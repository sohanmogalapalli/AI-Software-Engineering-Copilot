import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(10, 25, 47)        # #0A192F - Dominant Primary
    C_CARD = RGBColor(255, 255, 255)    # White card
    C_TEAL = RGBColor(0, 168, 150)      # #00A896 - Vibrant Accent
    C_BLUE = RGBColor(11, 60, 93)       # #0B3C5D - Deep Slate Blue
    C_GOLD = RGBColor(245, 166, 35)     # #F5A623 - Warm Highlight
    C_TEXT = RGBColor(34, 34, 34)       # Body text
    C_MUTED = RGBColor(100, 116, 139)   # Subtitles
    C_BG_LIGHT = RGBColor(244, 246, 249)# Light canvas
    C_BORDER = RGBColor(226, 232, 240)  # Borders

    def set_canvas_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, title_text, category_text="OPERATING SYSTEMS / AI PROJECT PRESENTATION"):
        # Header banner strip
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.1))
        banner.fill.solid()
        banner.fill.fore_color.rgb = C_NAVY
        banner.line.color.rgb = C_NAVY

        # Category tag
        p_cat = banner.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL
        p_cat.space_after = Pt(2)

        # Main Slide Title
        p_title = banner.text_frame.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(255, 255, 255)

        # Accent line below banner
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.1), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = C_TEAL
        line.line.color.rgb = C_TEAL

    def add_card(slide, left, top, width, height, title="", title_color=C_BLUE, bg_color=C_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(8)
        return card, tf

    def add_bullet(tf, bold_prefix, text, size=11, space_after=6, text_color=C_TEXT):
        p = tf.add_paragraph() if len(tf.paragraphs[0].text) > 0 else tf.paragraphs[0]
        p.space_after = Pt(space_after)
        
        r1 = p.add_run()
        r1.text = "• " + bold_prefix + " "
        r1.font.bold = True
        r1.font.size = Pt(size)
        r1.font.color.rgb = C_NAVY

        r2 = p.add_run()
        r2.text = text
        r2.font.bold = False
        r2.font.size = Pt(size)
        r2.font.color.rgb = text_color

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s1, C_NAVY)

    # Decorative accent bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.1), Inches(1.8), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_TEAL
    top_bar.line.color.rgb = C_TEAL

    # Main Title Frame
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.333), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p_sub0 = tf1.paragraphs[0]
    p_sub0.text = "PROJECT EVALUATION & REVIEW PRESENTATION (REVIEW 1 & 2)"
    p_sub0.font.size = Pt(12)
    p_sub0.font.bold = True
    p_sub0.font.color.rgb = C_TEAL
    p_sub0.space_after = Pt(10)

    p_main = tf1.add_paragraph()
    p_main.text = "Repository-Aware AI Software Engineering Copilot"
    p_main.font.size = Pt(30)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    p_main.space_after = Pt(8)

    p_desc = tf1.add_paragraph()
    p_desc.text = "Hierarchical AST Parsing, Call-Graph Dependency Analysis, and Hybrid Retrieval for Large-Scale Codebases"
    p_desc.font.size = Pt(16)
    p_desc.font.italic = True
    p_desc.font.color.rgb = RGBColor(203, 213, 225)

    # Team Box Left
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.7), Inches(5.4), Inches(1.9))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = RGBColor(17, 34, 64)
    team_box.line.color.rgb = C_TEAL
    team_box.line.width = Pt(1.5)
    tf_team = team_box.text_frame
    tf_team.margin_left = Inches(0.3)
    tf_team.margin_top = Inches(0.2)

    p_t_head = tf_team.paragraphs[0]
    p_t_head.text = "PROJECT TEAM MEMBERS"
    p_t_head.font.size = Pt(12)
    p_t_head.font.bold = True
    p_t_head.font.color.rgb = C_GOLD
    p_t_head.space_after = Pt(6)

    p_m1 = tf_team.add_paragraph()
    p_m1.text = "1. Mogalapalli Sohan  |  Reg No: 24BCE2625"
    p_m1.font.size = Pt(13)
    p_m1.font.bold = True
    p_m1.font.color.rgb = RGBColor(255, 255, 255)
    p_m1.space_after = Pt(4)

    p_m2 = tf_team.add_paragraph()
    p_m2.text = "2. Mogalapalli Rohan  |  Reg No: 24BCE2622"
    p_m2.font.size = Pt(13)
    p_m2.font.bold = True
    p_m2.font.color.rgb = RGBColor(255, 255, 255)

    # Academic Block Right
    acad_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.7), Inches(5.5), Inches(1.9))
    acad_box.fill.solid()
    acad_box.fill.fore_color.rgb = RGBColor(17, 34, 64)
    acad_box.line.color.rgb = RGBColor(51, 65, 85)
    acad_box.line.width = Pt(1)
    tf_acad = acad_box.text_frame
    tf_acad.margin_left = Inches(0.3)
    tf_acad.margin_top = Inches(0.2)

    p_a_head = tf_acad.paragraphs[0]
    p_a_head.text = "INSTITUTIONAL AFFILIATION"
    p_a_head.font.size = Pt(12)
    p_a_head.font.bold = True
    p_a_head.font.color.rgb = C_TEAL
    p_a_head.space_after = Pt(6)

    p_a1 = tf_acad.add_paragraph()
    p_a1.text = "Department of Computer Science and Engineering"
    p_a1.font.size = Pt(12.5)
    p_a1.font.color.rgb = RGBColor(241, 245, 249)
    p_a1.space_after = Pt(2)

    p_a2 = tf_acad.add_paragraph()
    p_a2.text = "School of Computer Science and Engineering"
    p_a2.font.size = Pt(11.5)
    p_a2.font.color.rgb = RGBColor(148, 163, 184)
    p_a2.space_after = Pt(4)

    p_a3 = tf_acad.add_paragraph()
    p_a3.text = "Course Project Evaluation (Total Marks: 30)"
    p_a3.font.size = Pt(11)
    p_a3.font.bold = True
    p_a3.font.color.rgb = C_GOLD

    # ==========================================
    # SLIDE 2: MOTIVATION & PROBLEM STATEMENT
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2, C_BG_LIGHT)
    add_header(s2, "Motivation & Problem Formulation", "Component 1: Problem & Motivation")

    _, tf2_1 = add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5), "Industry Motivation & Context")
    add_bullet(tf2_1, "Developer Cognitive Overhead: ", "Empirical studies report developers spend 50%–60% of their working hours navigating, reading, and tracing codebases rather than writing new logic [1], [2].")
    add_bullet(tf2_1, "Exponential Repository Scale: ", "Modern production software exceeds hundreds of thousands of lines of code across microservices, asynchronous calls, and multi-package setups [3].")
    add_bullet(tf2_1, "High Maintenance Bottlenecks: ", "Onboarding new software engineers and diagnosing regression bugs across deep caller-callee chains remain the costliest phases of the SDLC [4], [17].")
    add_bullet(tf2_1, "Enterprise Privacy Mandate: ", "Enterprises cannot transmit sensitive proprietary source code to public cloud APIs due to IP ownership, licensing, and compliance policies [15].")

    _, tf2_2 = add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), "Current LLM Failure Modes on Code")
    add_bullet(tf2_2, "1. Context Window Truncation: ", "Repositories exceed effective token context windows; naive truncation causes catastrophic 'lost-in-the-middle' loss [10].")
    add_bullet(tf2_2, "2. Scope Severance via Naive Chunking: ", "Fixed-character splitting severs functions from parent classes, decorators, and required namespace imports [11].")
    add_bullet(tf2_2, "3. Dense Embedding Imprecision: ", "Vector embeddings struggle to differentiate closely named software identifiers (e.g., getUserById vs getUsersById) [12], [23].")
    add_bullet(tf2_2, "4. Graph & Dependency Blindness: ", "Standard RAG treats code as flat text, ignoring caller-callee hierarchies, PageRank hubs, and circular imports [14], [22].")
    add_bullet(tf2_2, "5. Hallucination Without Line Citations: ", "Models fabricate nonexistent methods without verifiable file and line anchors.")

    # ==========================================
    # SLIDE 3: PROJECT OBJECTIVES
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3, C_BG_LIGHT)
    add_header(s3, "Project Technical Objectives", "Component 1: Target Goals & Scope")

    cards_data = [
        ("1. Multi-Language AST Parsing", "Deterministic concrete syntax tree extraction across 8 languages (Python, TypeScript, JS, Java, C++, C, Go, Rust) using native Tree-sitter parsers [11].", Inches(0.8), Inches(1.4)),
        ("2. Breadcrumb Scope Chunking", "Prefix code snippets with hierarchical headers (# File, # Class Scope, # Decorators, # Imports) to eradicate out-of-context retrieval.", Inches(6.8), Inches(1.4)),
        ("3. Tri-Modal Hybrid Retrieval (RRF)", "Unify dense semantic embeddings (FAISS nomic-embed), BM25 Okapi identifier tokenization, and exact symbol boosting via Reciprocal Rank Fusion [20].", Inches(0.8), Inches(4.2)),
        ("4. Program Graph Blast Radius", "Construct NetworkX directed call and import graphs to compute multi-hop change impact sets, circular cycles, and risk levels (LOW to CRITICAL) [14], [17].", Inches(6.8), Inches(4.2))
    ]

    for title, desc, l, t in cards_data:
        _, tf_card = add_card(s3, l, t, Inches(5.7), Inches(2.5), title, C_NAVY)
        p = tf_card.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 4: EXISTING SYSTEMS VS PROPOSED
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4, C_BG_LIGHT)
    add_header(s4, "Comparison: Existing Systems vs. Proposed Copilot", "Component 1: Existing Systems & Approaches")

    # Table
    t_shape = s4.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    table = t_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(2.3)
    table.columns[3].width = Inches(2.3)
    table.columns[4].width = Inches(2.633)

    t_headers = ["Key Feature / Metric", "Ripgrep / Ctags", "Naive RAG (LangChain)", "Cloud Copilots (GitHub)", "Proposed System (Our Work)"]
    for i, h in enumerate(t_headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    t_rows = [
        ("Chunking Strategy", "Regex token lines", "Fixed character/token limit", "Active editor buffer window", "AST Scope Breadcrumbs Enriched"),
        ("Retrieval Engine", "Pure Lexical Search", "Dense Vector Only", "Proprietary Cloud Heuristics", "Tri-Modal Hybrid (Dense + BM25 + Symbol RRF)"),
        ("Call Graph & Impact", "None", "None (Flat text)", "Limited single-file hops", "NetworkX Directed Graph + Multi-Hop Blast Radius"),
        ("Privacy & Execution", "100% Local (CLI)", "Cloud API (OpenAI/Anthropic)", "Cloud Third-Party Servers", "100% Local Inference (Ollama Qwen2.5-Coder)")
    ]

    for row_idx, data in enumerate(t_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY
            elif col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_BLUE
            else:
                p.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 5: LITERATURE SURVEY MATRIX
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5, C_BG_LIGHT)
    add_header(s5, "Literature Survey & Theoretical Foundations", "Component 1: Literature Survey (Google Scholar)")

    t5_shape = s5.shapes.add_table(6, 4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(2.2)
    t5.columns[1].width = Inches(3.6)
    t5.columns[2].width = Inches(2.9)
    t5.columns[3].width = Inches(3.033)

    t5_headers = ["Author & Venue", "Core Methodology & Contribution", "Key Strength", "Identified Research Gap"]
    for i, h in enumerate(t5_headers):
        cell = t5.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    t5_rows = [
        ("Ferrante et al. [14]\nACM TOPLAS", "Program Dependence Graphs (PDG) for control & data flow modeling", "Formal reachability and slicing guarantees", "Pure compiler optimization; no neural or vector search."),
        ("Kramer [11]\nACM SPLASH", "Incremental Tree-sitter parsing for multi-language software syntax trees", "Sub-millisecond AST updates across edits", "Parses syntax only; no semantic retrieval or LLM reasoning."),
        ("Gu et al. [12]\nIEEE/ACM ICSE", "Deep Code Search (DeepCS) using dual-encoder neural representations", "Learns high-level semantic developer intent", "Poor precision on exact identifier tokens and method definitions."),
        ("Robertson et al. [21]\nFoundations in IR", "Probabilistic BM25 Okapi lexical term frequency ranking framework", "Unmatched deterministic exact-token accuracy", "Completely fails on natural language synonyms and concepts."),
        ("Zhang et al. [3]\nEMNLP", "RepoCoder: Iterative retrieval-augmented generation for repositories", "Improves cross-file completion via sliding windows", "Lacks AST breadcrumb scope headers and call-graph blast analysis.")
    ]

    for row_idx, data in enumerate(t5_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t5.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY

    # ==========================================
    # SLIDE 6: PATENT PRIOR-ART MATRIX
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6, C_BG_LIGHT)
    add_header(s6, "Patent Prior-Art Analysis (Google Patents)", "Component 1: Patent-Track Evaluation")

    t6_shape = s6.shapes.add_table(6, 4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(4.3))
    t6 = t6_shape.table
    t6.columns[0].width = Inches(2.0)
    t6.columns[1].width = Inches(1.8)
    t6.columns[2].width = Inches(3.9)
    t6.columns[3].width = Inches(4.033)

    t6_headers = ["Patent / Pub. No.", "Assignee (Year)", "Disclosed Invention Description", "Key Differentiation in Our System"]
    for i, h in enumerate(t6_headers):
        cell = t6.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    t6_rows = [
        ("US11,288,046 B2 [25]", "Microsoft (2022)", "Synthesizing code using neural networks and local file context", "Relies on flat text buffers; lacks AST breadcrumb metadata injection into embeddings."),
        ("US11,768,918 B1 [26]", "Amazon (2023)", "Code completion using language models conditioned on repository metadata", "Targets token autocompletion; does not build directed call graphs for blast radius risk estimation."),
        ("US2023/0385367 A1 [27]", "Google LLC (2023)", "Semantic code search using dual-encoder vector embeddings", "Dense-only; lacks hybrid Reciprocal Rank Fusion with exact AST symbol boost."),
        ("US10,846,063 B2 [28]", "IBM Corp (2020)", "Static dependency analysis for microservice impact assessment", "Pure static rule analysis; lacks generative RAG reasoning and interactive natural language QA."),
        ("US11,487,516 B1 [29]", "Meta (2022)", "Automated change analysis utilizing call graph traversal", "Focuses on build failure regression; does not integrate local LLM prompt grounding or breadcrumbs.")
    ]

    for row_idx, data in enumerate(t6_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t6.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY

    # Protectable claims box below
    _, tf_claim = add_card(s6, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.2), "Potentially Protectable Novel Claims (Invention Summary)", C_GOLD)
    add_bullet(tf_claim, "Claim 1: ", "Context-Enriched Breadcrumb Chunk Injection: Recursively prepending AST scopes into vector embedding payloads.", 9.5, 2)
    add_bullet(tf_claim, "Claim 2: ", "Tri-Modal Reciprocal Rank Fusion: Fusing dense vectors, lexical BM25, and exact AST symbol matches with calibrated code weights.", 9.5, 2)
    add_bullet(tf_claim, "Claim 3: ", "Graph-Augmented Blast-Radius Impact Grounding: Mapping directed call reachability to risk tiers for predictive LLM reasoning.", 9.5, 2)

    # ==========================================
    # SLIDE 7: SYSTEM ARCHITECTURE DIAGRAM
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7, C_BG_LIGHT)
    add_header(s7, "Proposed System Architecture", "Component 2: System Architecture & Workflow")

    # Add diagram image
    img_path = "architecture_diagram.png"
    if os.path.exists(img_path):
        s7.shapes.add_picture(img_path, Inches(0.8), Inches(1.3), Inches(8.0), Inches(5.8))

    # Right explanations
    _, tf7 = add_card(s7, Inches(9.0), Inches(1.3), Inches(3.533), Inches(5.8), "Pipeline Core Modules", C_NAVY)
    add_bullet(tf7, "1. Ingestion & AST: ", "Tree-sitter concrete syntax parsing across 8 languages.", 10, 8)
    add_bullet(tf7, "2. Breadcrumbs: ", "Enriched metadata headers prepended to code snippets.", 10, 8)
    add_bullet(tf7, "3. Program Graph: ", "NetworkX directed graph for call chains & PageRank hubs.", 10, 8)
    add_bullet(tf7, "4. Dual Index: ", "FAISS (nomic-embed) + BM25 Okapi with identifier tokenizer.", 10, 8)
    add_bullet(tf7, "5. RRF Blender: ", "Tri-modal Reciprocal Rank Fusion prioritizing exact symbols.", 10, 8)
    add_bullet(tf7, "6. Local Reasoning: ", "Streaming RAG & ReAct Agent powered by Ollama Qwen2.5-Coder.", 10, 8)

    # ==========================================
    # SLIDE 8: MATHEMATICAL FORMULATIONS
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s8, C_BG_LIGHT)
    add_header(s8, "Algorithms & Mathematical Formulations", "Component 2: Core Formulations")

    _, tf8_1 = add_card(s8, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5), "Tri-Modal Reciprocal Rank Fusion (RRF)")
    add_bullet(tf8_1, "Mathematical Objective: ", "Eliminates score calibration discrepancies between cosine similarities and BM25 unbounded scores [20].")
    
    p_f1 = tf8_1.add_paragraph()
    p_f1.text = "Score_RRF(d) = \n  [ w_dense / (k + rank_dense(d)) ]\n+ [ w_bm25 / (k + rank_bm25(d)) ]\n+ [ w_sym / (k + rank_sym(d)) ]"
    p_f1.font.bold = True
    p_f1.font.size = Pt(13)
    p_f1.font.color.rgb = C_BLUE
    p_f1.space_after = Pt(10)

    add_bullet(tf8_1, "Smoothing Factor: ", "k = 60 prevents high-rank distortion.", 11, 6)
    add_bullet(tf8_1, "Empirical Weights: ", "w_dense = 1.0 (intent), w_bm25 = 0.8 (tokens), w_sym = 1.2 (symbol definitions).", 11, 6)
    add_bullet(tf8_1, "Exact Symbol Guarantee: ", "Exact method signatures immediately rise to Top-1 rank.", 11, 6)

    _, tf8_2 = add_card(s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), "Graph Blast-Radius & Impact Assessment")
    add_bullet(tf8_2, "Reachability Formulation: ", "Let G = (V, E) be the directed dependency graph [14], [22].")

    p_f2 = tf8_2.add_paragraph()
    p_f2.text = "Impact(s, D) = \n{ v in V | exists path s ->* v with length <= D }"
    p_f2.font.bold = True
    p_f2.font.size = Pt(13)
    p_f2.font.color.rgb = C_BLUE
    p_f2.space_after = Pt(10)

    add_bullet(tf8_2, "Risk Classification Engine [17], [18]:", "", 11, 4)
    add_bullet(tf8_2, "• CRITICAL: ", "|Impact| >= 15 or symbol in top 5% PageRank.", 10.5, 4)
    add_bullet(tf8_2, "• HIGH: ", "8 <= |Impact| < 15 downstream modules.", 10.5, 4)
    add_bullet(tf8_2, "• MEDIUM: ", "3 <= |Impact| < 8 downstream modules.", 10.5, 4)
    add_bullet(tf8_2, "• LOW: ", "|Impact| < 3 (localized changes).", 10.5, 4)

    # ==========================================
    # SLIDE 9: EXPERIMENTAL RESULTS
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s9, C_BG_LIGHT)
    add_header(s9, "Experimental Results & Validation", "Component 3: Implementation & Validation")

    # Table Left: Accuracy
    t9_shape = s9.shapes.add_table(5, 5, Inches(0.8), Inches(1.4), Inches(6.8), Inches(3.5))
    t9 = t9_shape.table
    t9.columns[0].width = Inches(2.4)
    t9.columns[1].width = Inches(1.1)
    t9.columns[2].width = Inches(1.1)
    t9.columns[3].width = Inches(1.1)
    t9.columns[4].width = Inches(1.1)

    t9_headers = ["Retrieval Strategy", "P@1 (%)", "P@5 (%)", "R@5 (%)", "MRR@10"]
    for i, h in enumerate(t9_headers):
        cell = t9.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    t9_rows = [
        ("Dense Vector Only (FAISS)", "68.4", "74.2", "71.5", "0.724"),
        ("Lexical Only (BM25)", "61.2", "69.8", "66.2", "0.658"),
        ("Hybrid (Simple Average)", "76.5", "82.1", "79.4", "0.789"),
        ("Proposed Hybrid (RRF)", "89.7", "94.3", "92.8", "0.912")
    ]

    for row_idx, data in enumerate(t9_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t9.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(230, 246, 245) if row_idx == 4 else (RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255))
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if row_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_TEAL if col_idx > 0 else C_NAVY
            if col_idx > 0:
                p.alignment = PP_ALIGN.CENTER

    # Table Right: Latency
    t9_lat = s9.shapes.add_table(7, 3, Inches(7.9), Inches(1.4), Inches(4.6), Inches(3.5))
    t9_l = t9_lat.table
    t9_l.columns[0].width = Inches(2.2)
    t9_l.columns[1].width = Inches(1.3)
    t9_l.columns[2].width = Inches(1.1)

    t9_l_headers = ["Pipeline Stage", "Mechanism", "Latency"]
    for i, h in enumerate(t9_l_headers):
        cell = t9_l.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    t9_l_rows = [
        ("AST Entity Parsing", "Tree-sitter", "42 ms / 1k"),
        ("Embedding Gen (x10)", "nomic-embed", "185 ms"),
        ("Dual-Index Search", "FAISS + BM25", "18 ms"),
        ("Blast Radius BFS", "NetworkX", "6 ms"),
        ("Time to First Token", "Ollama Qwen2.5", "310 ms"),
        ("Cumulative Response", "Streaming RAG", "~560 ms")
    ]

    for row_idx, data in enumerate(t9_l_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t9_l.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(230, 246, 245) if row_idx == 6 else (RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255))
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            if row_idx == 6:
                p.font.bold = True
                p.font.color.rgb = C_TEAL if col_idx > 0 else C_NAVY
            if col_idx > 0:
                p.alignment = PP_ALIGN.CENTER

    # Bottom summary card
    _, tf9_b = add_card(s9, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8), "Key Validation Takeaways", C_BLUE)
    add_bullet(tf9_b, "Significant MRR Gains: ", "Proposed Tri-Modal RRF achieves 0.912 MRR@10, outperforming dense search (0.724) and BM25 (0.658).", 10.5, 3)
    add_bullet(tf9_b, "Low Interactive Latency: ", "First token streamed in ~310 ms; full grounded answer synthesized in ~560 ms on standard workstation.", 10.5, 3)
    add_bullet(tf9_b, "Grounded Precision: ", "Breadcrumb chunking guarantees 94.3% top-5 retrieval precision with 0 hallucinations on cited lines.", 10.5, 3)

    # ==========================================
    # SLIDE 10: RUBRIC COMPLIANCE (30 MARKS)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s10, C_BG_LIGHT)
    add_header(s10, "Review 1 & 2 Rubric Compliance (Marks: 30)", "Rubric Evaluation Alignment")

    t10_shape = s10.shapes.add_table(4, 4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4))
    t10 = t10_shape.table
    t10.columns[0].width = Inches(2.2)
    t10.columns[1].width = Inches(3.1)
    t10.columns[2].width = Inches(3.2)
    t10.columns[3].width = Inches(3.233)

    t10_headers = ["Rubric Component", "Common Deliverables", "Conference Paper Track", "Patent Track Deliverables"]
    for i, h in enumerate(t10_headers):
        cell = t10.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    t10_rows = [
        ("Component 1:\nProblem & Literature\n(Review 1 - 10 Marks)", "Title, Problem Statement, Motivation, Objectives, Existing System, Literature Survey, Research Gap.", "Survey of 24 Google Scholar papers [1]–[24], analytical comparison, and contribution claims.", "Prior-art study of 5 Google Patents [25]–[29], novelty identification, protectable claims."),
        ("Component 2:\nProposed Methodology\n(Review 2)", "Proposed Architecture (Fig. 1), workflow, modules, algorithms, technologies.", "AST breadcrumb method, Tri-Modal RRF (Eq. 1), and NetworkX call graph blast radius (Eq. 2).", "Detailed invention architecture, novel mechanism description, and protectable claims 1–3."),
        ("Component 3:\nValidation & Prototype", "Implementation status, screenshots, experimental setup, latency profile.", "Benchmark evaluation, baseline comparison (Table III), precision/recall metrics.", "Working local prototype demonstration and empirical validation evidence.")
    ]

    for row_idx, data in enumerate(t10_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t10.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY

    # ==========================================
    # SLIDE 11: CONCLUSION & FUTURE SCOPE
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s11, C_NAVY)

    # Header in dark slide
    top_bar_c = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.0), Inches(1.8), Inches(0.08))
    top_bar_c.fill.solid()
    top_bar_c.fill.fore_color.rgb = C_TEAL
    top_bar_c.line.color.rgb = C_TEAL

    t_box_c = s11.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(1.2))
    tf11 = t_box_c.text_frame
    p_c1 = tf11.paragraphs[0]
    p_c1.text = "CONCLUSION & FUTURE SCOPE"
    p_c1.font.size = Pt(24)
    p_c1.font.bold = True
    p_c1.font.color.rgb = RGBColor(255, 255, 255)

    # Card Left: Summary
    card_c1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.4), Inches(5.4), Inches(4.3))
    card_c1.fill.solid()
    card_c1.fill.fore_color.rgb = RGBColor(17, 34, 64)
    card_c1.line.color.rgb = C_TEAL
    tf_c1 = card_c1.text_frame
    tf_c1.margin_left = Inches(0.3)
    tf_c1.margin_top = Inches(0.25)
    
    p_h1 = tf_c1.paragraphs[0]
    p_h1.text = "Key Project Achievements"
    p_h1.font.size = Pt(14)
    p_h1.font.bold = True
    p_h1.font.color.rgb = C_GOLD
    p_h1.space_after = Pt(8)

    add_bullet(tf_c1, "Deterministic Grounding: ", "Coupled Tree-sitter ASTs with breadcrumb injection to guarantee 94.3% top-5 retrieval precision.", 11, 8, RGBColor(241, 245, 249))
    add_bullet(tf_c1, "High-Precision Ranking: ", "Tri-Modal RRF achieves 0.912 MRR@10, outperforming standalone vector and keyword engines.", 11, 8, RGBColor(241, 245, 249))
    add_bullet(tf_c1, "Change Blast Radius: ", "NetworkX directed graph evaluates multi-hop ripple effects and categorizes risk tiers.", 11, 8, RGBColor(241, 245, 249))
    add_bullet(tf_c1, "100% Local Privacy: ", "Air-gapped execution via Ollama (Qwen2.5-Coder:7b) with zero third-party cloud data leakage.", 11, 8, RGBColor(241, 245, 249))

    # Card Right: Future Scope
    card_c2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.4), Inches(5.5), Inches(4.3))
    card_c2.fill.solid()
    card_c2.fill.fore_color.rgb = RGBColor(17, 34, 64)
    card_c2.line.color.rgb = RGBColor(51, 65, 85)
    tf_c2 = card_c2.text_frame
    tf_c2.margin_left = Inches(0.3)
    tf_c2.margin_top = Inches(0.25)

    p_h2 = tf_c2.paragraphs[0]
    p_h2.text = "Future Research Directions"
    p_h2.font.size = Pt(14)
    p_h2.font.bold = True
    p_h2.font.color.rgb = C_TEAL
    p_h2.space_after = Pt(8)

    add_bullet(tf_c2, "Dynamic Runtime Profiling: ", "Integrate eBPF and runtime telemetry to merge static call graphs with dynamic execution traces.", 11, 8, RGBColor(241, 245, 249))
    add_bullet(tf_c2, "Automated Test Synthesis: ", "Leverage blast-radius impact sets to automatically synthesize regression unit tests [24].", 11, 8, RGBColor(241, 245, 249))
    add_bullet(tf_c2, "Multi-Agent Refactoring: ", "Deploy cooperative agent teams for automated multi-file code repairs and pull requests.", 11, 8, RGBColor(241, 245, 249))
    add_bullet(tf_c2, "IDE Extension Ecosystem: ", "Package the backend into lightweight VS Code and JetBrains LSP sidecars.", 11, 8, RGBColor(241, 245, 249))

    # Save presentation
    output_pptx = "AI_Software_Engineering_Copilot_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation generated successfully: {output_pptx}")

if __name__ == "__main__":
    create_deck()
