import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="PNR–IDIR Analysis", layout="wide")

# ------------------- CUSTOM CSS FOR TABLES -------------------
st.markdown("""
<style>

/* ------------------------------------------------------ */
/*                 TABLE + AG GRID STYLING                */
/* ------------------------------------------------------ */

/* AG-Grid Header */
[data-testid="stDataFrame"] .ag-header {
    background-color: #E6D7FF !important;
    color: #4A148C !important;
    font-weight: 800 !important;
    font-size: 15px !important;
}

/* AG-Grid Header Cell */
[data-testid="stDataFrame"] .ag-header-cell-label {
    color: #4A148C !important;
    justify-content: center !important;
}
[data-testid="stDataFrame"] .ag-header-cell {
    text-align: center !important;
}

/* AG-Grid Body Cells */
[data-testid="stDataFrame"] .ag-cell {
    justify-content: center !important;
    text-align: center !important;
    font-size: 14px !important;
}

/* Row Hover Highlight */
[data-testid="stDataFrame"] .ag-row-hover {
    background-color: #F3E8FF !important;
}

/* HTML Table Header */
thead tr th {
    background-color: #E6D7FF !important;
    color: #4A235A !important;
    font-weight: 700 !important;
    text-align: center !important;
    border-bottom: 2px solid #B795D7 !important;
}

/* HTML Table Body */
tbody tr td {
    text-align: center !important;
}
tbody tr:hover {
    background-color: #F3E8FF !important;
}

/* ------------------------------------------------------ */
/* ⭐ First Column in Purple for All Tables (AG + HTML)    */
/* ------------------------------------------------------ */

/* First column — AG Grid */
[data-testid="stDataFrame"] .ag-center-cols-container .ag-row .ag-cell:first-child {
    background-color: #E6D7FF !important;
    color: #4A148C !important;
    font-weight: 700 !important;
}

/* First column — HTML Table */
table tbody tr td:first-child {
    background-color: #E6D7FF !important;
    color: #4A148C !important;
    font-weight: 700 !important;
}

/* First-column header */
[data-testid="stDataFrame"] .ag-header-cell:first-child .ag-header-cell-label,
table thead tr th:first-child {
    background-color: #E6D7FF !important;
    color: #4A148C !important;
    font-weight: 800 !important;
}

/* ------------------------------------------------------ */
/*                Section Title Styling                    */
/* ------------------------------------------------------ */
.section-title {
    font-size: 30px;
    font-weight: 700;
    color: #6A1B9A;
    padding-bottom: 8px;
}
.sub-heading {
    font-size: 22px;
    font-weight: 600;
    color: #8E44AD;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# ------------------- PAGE TITLE -------------------
st.markdown('<div class="section-title">📊 PNR–IDIR Classroom Interaction Analysis</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("📥 Upload your Speaker Excel File", type=["xlsx"])

if uploaded is not None:

    df = pd.read_excel(uploaded)
    df.index = df.index + 1

    # ASSUME SPEAKER COLUMN EXISTS OR CREATE IT IF NOT
    if "Speakers" not in df.columns:
        df["Speakers"] = df.index

    st.markdown('<div class="sub-heading">📄 Preview of Uploaded File</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    # ------------------- FORMULA DISPLAY -------------------
    st.markdown("""
    ### 📘 Computation Formulas
    - **PNR = Response / Instruction**  
    - **IDIR = (Response + Question) / (Lecture + Instruction)**  
    """)

    # ------------------- COMPUTE -------------------
    df["pnr"] = df["Response"] / df["Instruction"]
    df["idir"] = (df["Response"] + df["Question"]) / (df["Lecture"] + df["Instruction"])

    # ------------------- RANGE SUMMARY -------------------
    max_pnr = df["pnr"].max()
    min_pnr = df["pnr"].min()
    max_idir = df["idir"].max()
    min_idir = df["idir"].min()

    st.markdown('<div class="sub-heading">📌 PNR–IDIR Range Summary</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔼 Max PNR", f"{max_pnr:.3f}")
    col2.metric("🔽 Min PNR", f"{min_pnr:.3f}")
    col3.metric("🔼 Max IDIR", f"{max_idir:.3f}")
    col4.metric("🔽 Min IDIR", f"{min_idir:.3f}")

    # ------------------- CALCULATED TABLE -------------------
    st.markdown('<div class="sub-heading">🧮 Computed PNR and IDIR Values</div>', unsafe_allow_html=True)
    df_display = df.rename(columns={"pnr": "PNR", "idir": "IDIR"})
    st.dataframe(df_display, use_container_width=True)


    # ------------------- QUADRANT LOGIC -------------------
    def assign_quadrant(row):
        if row["pnr"] >= 1 and row["idir"] >= 1:
            return "Q1"
        elif row["pnr"] < 1 and row["idir"] >= 1:
            return "Q2"
        elif row["pnr"] < 1 and row["idir"] < 1:
            return "Q3"
        else:
            return "Q4"

    df["Quadrant"] = df.apply(assign_quadrant, axis=1)

    # ------------------- QUADRANT DESCRIPTIONS -------------------
    st.markdown("""
    ### 🧭 Quadrant Interpretation Guide

    #### 🔴 Q1 — High PNR, High IDIR  
    Strong student-centric environment  

    #### 🔵 Q2 — Low PNR, High IDIR  
    Good questioning but low encouragement  

    #### 🟣 Q3 — Low PNR, Low IDIR  
    Teacher-dominated  

    #### 🟠 Q4 — High PNR, Low IDIR  
    Encouraging but lecture-heavy  
    """)

    # ------------------- COLORS -------------------
    quadrant_colors = {
        "Q1": "red",
        "Q2": "lightskyblue",
        "Q3": "blue",
        "Q4": "pink"
    }

    # ------------------- FIGURE 1 -------------------
    # ------------------- FIGURE 1 -------------------
    st.markdown('<div class="sub-heading">📈 Graph 1 — Full IDIR–PNR Plot</div>', unsafe_allow_html=True)

    fig1 = px.scatter(
        df, x="idir", y="pnr",
        color="Quadrant",
        text="Speakers",
        color_discrete_map=quadrant_colors,
        hover_data=["Speakers", "pnr", "idir", "Quadrant"]
    )

    fig1.update_traces(textposition="top center")
    fig1.add_hline(y=1, line_dash="dash", line_width=1)
    fig1.add_vline(x=1, line_dash="dash", line_width=1)
    fig1.update_xaxes(title="IDIR")
    fig1.update_yaxes(title="PNR")

    st.plotly_chart(fig1, use_container_width=True)

    # ------------------- FIGURE 2 (Q1 ONLY) -------------------
    # ------------------- FIGURE 2 (Q1 ONLY) -------------------
    st.markdown('<div class="sub-heading">📈 Graph 2 — Only Q1 Region (IDIR–PNR)</div>', unsafe_allow_html=True)

    df_q1 = df[(df["pnr"] >= 1) & (df["idir"] >= 1)]

    fig2 = px.scatter(
        df_q1, x="idir", y="pnr",
        color="Quadrant",
        text="Speakers",
        color_discrete_map=quadrant_colors,
        hover_data=["Speakers", "pnr", "idir", "Quadrant"]
    )

    fig2.update_traces(textposition="top center")
    fig2.add_hline(y=1, line_dash="dash", line_width=1)
    fig2.add_vline(x=1, line_dash="dash", line_width=1)
    fig2.update_xaxes(title="IDIR")
    fig2.update_yaxes(title="PNR")

    st.plotly_chart(fig2, use_container_width=True)


    # ------------------- CLASSROOM BALANCE INDEX (CBI) -------------------
    st.markdown('<div class="sub-heading">📘 Classroom Balance Index (CBI)</div>', unsafe_allow_html=True)

    st.markdown("""
        ### 📐 Formula  
        CBI = α × PNR + β × IDIR  
        Where:  
        - α = **0.45**  
        - β = **0.55**
    """)

    df_cbi = df_q1.copy()
    df_cbi["CBI"] = (0.45 * df_cbi["pnr"]) + (0.55 * df_cbi["idir"])
    df_cbi_sorted = df_cbi.sort_values(by="CBI", ascending=False)

    st.markdown("### 🧮 Classroom Balance Index Table (Q1 Only)")
    df_display = df.rename(columns={"pnr": "PNR", "idir": "IDIR"})
    st.dataframe(df_display, use_container_width=True)


    # ---------------------------------------------------------
    # 📌 ADVANCED CBI ANALYSIS — 4 Experiments with Dynamic α & β
    # ---------------------------------------------------------
    st.markdown('<div class="sub-heading">🧮 Advanced CBI Experiments</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 📘 CBI Formula  
    CBI = α × PNR + β × IDIR  
    Enter **α and β for 4 experiments** (α + β = 1).
    """)

    with st.expander("⚙️ Enter Alpha (α) and Beta (β) for 4 Experiments"):
        colA1, colB1 = st.columns(2)
        alpha1 = colA1.number_input("α₁", 0.0, 1.0, 0.45, 0.01)
        beta1 = colB1.number_input("β₁", 0.0, 1.0, 0.55, 0.01)

        colA2, colB2 = st.columns(2)
        alpha2 = colA2.number_input("α₂", 0.0, 1.0, 0.40, 0.01)
        beta2 = colB2.number_input("β₂", 0.0, 1.0, 0.60, 0.01)

        colA3, colB3 = st.columns(2)
        alpha3 = colA3.number_input("α₃", 0.0, 1.0, 0.35, 0.01)
        beta3 = colB3.number_input("β₃", 0.0, 1.0, 0.65, 0.01)

        colA4, colB4 = st.columns(2)
        alpha4 = colA4.number_input("α₄", 0.0, 1.0, 0.30, 0.01)
        beta4 = colB4.number_input("β₄", 0.0, 1.0, 0.70, 0.01)

    df_exp = df.copy()
    df_exp["EXP1"] = alpha1 * df_exp["pnr"] + beta1 * df_exp["idir"]
    df_exp["EXP2"] = alpha2 * df_exp["pnr"] + beta2 * df_exp["idir"]
    df_exp["EXP3"] = alpha3 * df_exp["pnr"] + beta3 * df_exp["idir"]
    df_exp["EXP4"] = alpha4 * df_exp["pnr"] + beta4 * df_exp["idir"]

    st.markdown("### 📊 Experiment Results Table")
    st.dataframe(
        df_exp[["Speakers", "pnr", "idir", "EXP1", "EXP2", "EXP3", "EXP4"]],
        use_container_width=True
    )

    st.markdown('<div class="sub-heading">📈 Comparison of 4 CBI Experiments</div>', unsafe_allow_html=True)
    fig = px.line(
        df_exp,
        x="Speakers",
        y=["EXP1", "EXP2", "EXP3", "EXP4"],
        markers=True,
        title="CBI Experiment Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)


    # ---------------------------------------------------------
    # 📊 Ranked Classroom Balance Index Table (After Plot)
    # ---------------------------------------------------------
    st.markdown("### 🏆 Ranked Classroom Balance Index")

    # Calculate combined ranking score (mean of 4 experiments)
    df_rank = df_exp.copy()
    df_rank["Ranked Classroom Balance Index"] = df_rank[["EXP1", "EXP2", "EXP3", "EXP4"]].mean(axis=1)

    # Sort in descending order
    df_rank_sorted = df_rank.sort_values(by="Ranked Classroom Balance Index", ascending=False)

    # Rename pnr and idir for display (optional)
    df_rank_display = df_rank_sorted.rename(columns={"pnr": "PNR", "idir": "IDIR"})

    # Display final ranked table
    st.dataframe(
        df_rank_display[
            ["Speakers", "PNR", "IDIR", "EXP1", "EXP2", "EXP3", "EXP4", "Ranked Classroom Balance Index"]
        ],
        use_container_width=True
    )

else:
    st.info("📥 Please upload an Excel file to begin.")
