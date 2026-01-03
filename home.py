import streamlit as st

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Classroom Interaction Analysis System",
    page_icon="🎓",
    layout="wide"
)
# st.sidebar.markdown("<div class='sidebar-title'>📚 Navigation</div>", unsafe_allow_html=True)

# ------------------------------------------------
# CUSTOM CSS FOR BETTER UI
# ------------------------------------------------
st.markdown("""
    <style>

        /* Remove default padding */
        .main {
            padding: 0rem 2rem;
        }

        /* Card styling */
        .info-card {
            background: #f3eaff;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
            border-left: 6px solid #8b4cea;
        }

        /* Title styling */
        .title {
            font-size: 46px;
            font-weight: 700;
            text-align: center;
            margin-top: 10px;
            color: #333;
        }

        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #7b3fe0;
            margin-bottom: 35px;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #f5f0ff;
            padding-top: 20px;
        }
        
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #4b2ca0;
            padding-bottom: 15px;
            text-align: center;
        }
        
        /* Sidebar menu */
        .sidebar-link {
            padding: 10px 15px;
            margin: 6px 0;
            border-radius: 10px;
            color: #4b2ca0;
            font-size: 18px;
            font-weight: 500;
            text-decoration: none;
            display: block;
        }

        .sidebar-link:hover {
            background-color: #e2d4ff;
            color: #3b1b85;
        }

    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------

# st.sidebar.markdown("<a class='sidebar-link' href='/Home' target='_self'>🏠 Home</a>", unsafe_allow_html=True)
# st.sidebar.markdown("<a class='sidebar-link' href='/app' target='_self'>📊 Model Prediction</a>", unsafe_allow_html=True)
# st.sidebar.markdown("<a class='sidebar-link' href='/PNR_IDIR_Analysis' target='_self'>📈 PNR & IDIR Analysis</a>", unsafe_allow_html=True)

# ------------------------------------------------
# MAIN CONTENT
# ------------------------------------------------
st.markdown("<div class='title'>🎓 Classroom Interaction Analysis System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered System for Classroom Transcript Understanding</div>", unsafe_allow_html=True)

# ------------------------------------------------
# PROJECT OVERVIEW CARD
# ------------------------------------------------
st.markdown("<div class='info-card'>", unsafe_allow_html=True)
st.markdown("""
### 📘 **Application Overview**

Classroom interaction plays a crucial role in shaping learning experiences, yet analysing it 
objectively has always been challenging. Traditional observation methods suffer from 
subjectivity and limited scalability. This system addresses these challenges using an 
AI-driven, automated pipeline built on modern **Deep Learning and NLP**.

---

### 🔍 **What the System Does**
- 🧠 Processes classroom transcripts automatically  
- 📝 Classifies every utterance into **Lecture, Question, Instruction, Response** using  
  fine-tuned **BERT and RoBERTa** transformer models  
- 📊 Quantifies interaction dynamics using two key behavioural ratios:  
  - **PNR**: Positive-to-Negative Reinforcement  
  - **IDIR**: Indirect-to-Direct Influence  

Low values (<1) indicate **teacher-centric behaviour**, whereas values ≥1 show a shift 
toward **student-centric engagement**.

---

### 🎯 **Introducing: Classroom Balance Index (CBI)**
To capture overall classroom orientation, we propose a new metric:  
**CBI = 0.45 × PNR + 0.55 × IDIR**,  
inspired by theories of social learning, constructivism, cognitive development, and learner 
autonomy.  
CBI offers a single, continuous measure of student-centeredness.

---

### 📈 **Why It Matters**
The system provides:
- ✔ Automated, scalable transcript analysis  
- ✔ Objective interpretation of teaching–learning patterns  
- ✔ A **four-quadrant visual model** revealing teacher-centric vs student-centric behaviour  
- ✔ Clear insights aligned with **NEP 2020’s learner-centric vision**

---

### 🌐 **Complete Web-Based Solution**
A user-friendly platform integrates:
- NLP-powered classification  
- PNR, IDIR & CBI computation  
- Interactive dashboards and quadrant visualizations  

This enables teachers, researchers, and observers to reflect on classroom communication and 
enhance pedagogical quality.

---

### 🚀 **Impact**
By combining **transformer-based NLP**, behavioural metrics, and intuitive visualization, this 
project offers a powerful digital tool for evidence-based classroom analysis. It bridges 
education, computer science, and learning analytics—supporting improved instructional design 
and promoting student-centric learning.
""")



st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("### ")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>Developed By Ritu Soni </center>", unsafe_allow_html=True)
