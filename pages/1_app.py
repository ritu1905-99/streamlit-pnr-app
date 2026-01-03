import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from inference import classify_text, predict_label
from io import BytesIO

st.set_page_config(page_title="Classroom Interaction Analysis", layout="wide")

# ------------------- HEADER + CUSTOM CSS -------------------
st.markdown("""
<style>
.big-title {
    font-size: 50px;
    font-weight: 700;
    color: #2A4D69;
    text-align: center;
}
.sub-title {
    font-size: 20px;
    font-weight: 400;
    color: #4F6D7A;
    text-align: center;
    margin-top: -15px;
}
.section-title {
    font-size: 25px;
    font-weight: 600;
    color: #1F4E79;
    padding-top: 15px;
}
.box {
    padding: 20px;
    background-color: #F2F4F8;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* -------- Purple heading for Preview of Uploaded File -------- */
.preview-title {
    font-size: 22px;
    font-weight: 600;
    color: #6A1B9A;
    margin-top: 20px;
}

thead tr th {
    background-color: #E8DAEF !important;
    color: #4A235A !important;
    font-weight: 700 !important;
}

table {
    border-radius: 12px !important;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎓 Classroom Interaction Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Classroom Interaction Classification System</div><br>', unsafe_allow_html=True)


# ====================================================
# 🔷 SECTION 1 — Single Text Prediction
# ====================================================
st.markdown('<div class="section-title">📝 Single Sentence Classification</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    text = st.text_area("Enter a classroom utterance:", height=150)

    if st.button("Predict Label"):
        if text.strip() == "":
            st.warning("⚠️ Please enter some text.")
        else:
            label, confidence = classify_text(text)
            st.success(f"**Predicted Class:** {label}")
            st.info(f"**Confidence Score:** `{confidence:.4f}`")

    st.markdown('</div>', unsafe_allow_html=True)


# ====================================================
# 🔷 SECTION 2 — Manual 5 Inputs
# ====================================================
st.markdown('<div class="section-title">🧪 Test Manual Inputs (5 Examples)</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    for i in range(5):
        st.markdown(f"#### Example {i+1}")
        col1, col2 = st.columns(2)

        role = col1.selectbox(f"Role {i+1}", ["Teacher", "Student"], key=f"role_{i}")
        utt = col2.text_input(f"Utterance {i+1}", key=f"utt_{i}")

        if utt:
            # 🔥 Updated: Now get label + confidence
            label, confidence = classify_text(utt)

            st.write(
                f"🔮 **Predicted Label:** {label}  &nbsp;&nbsp; | &nbsp;&nbsp; "
                f"🔢 **Confidence:** `{confidence:.4f}`"
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# 🔷 SECTION 3 — Excel Upload + Prediction
# ====================================================
st.markdown('<div class="section-title">📂 Excel File Classification</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if excel_file is not None:
        df = pd.read_excel(excel_file)

        # ---------- Preview ----------
        st.markdown('<div class="preview-title">📄 Preview of Uploaded File</div>', unsafe_allow_html=True)
        df_display = df.head().reset_index(drop=True)

        def style_table(df_in):
            styles = [
                {"selector": "thead th", "props": [
                    ("background-color", "#E8DAEF"),
                    ("color", "#4A235A"),
                    ("font-weight", "700"),
                    ("font-size", "14px"),
                    ("padding", "6px")
                ]},
                {"selector": "tbody td", "props": [
                    ("background-color", "#FFFFFF"),
                    ("color", "#1B2631"),
                    ("padding", "6px"),
                    ("border-bottom", "1px solid #E5E7EB")
                ]}
            ]
            return df_in.style.set_table_styles(styles).set_properties(**{"text-align": "left"})

        st.markdown(style_table(df_display).to_html(), unsafe_allow_html=True)

        # ================= VALIDATION =================
        if "Role" not in df.columns or "Utterance" not in df.columns:
            st.error("❌ Excel must contain **Role** and **Utterance** columns!")
        else:
            if st.button("Run Excel Predictions"):
                st.info("🔍 Classifying all rows... Please wait.")

                # Run predictions
                df["Predicted_Label"] = df.apply(
                    lambda row: predict_label(str(row["Role"]), str(row["Utterance"])),
                    axis=1
                )

                st.success("✅ Classification Completed!")


                # =========================================================
                # 🔥 NEW SECTION — DATA VISUALIZATION
                # =========================================================
                st.markdown('<div class="section-title">📊 Data Visualization</div>', unsafe_allow_html=True)
                st.markdown('<div class="box">', unsafe_allow_html=True)

                # ---- Total Utterances ----
                total_utter = len(df)
                teacher_utter = len(df[df["Role"].str.lower() == "teacher"])
                student_utter = len(df[df["Role"].str.lower() == "student"])

                colA, colB, colC = st.columns(3)
                colA.metric("🗂 Total Utterances", total_utter)
                colB.metric("👩‍🏫 Teacher Utterances", teacher_utter)
                colC.metric("👧 Student Utterances", student_utter)

                # ---- Predicted Label Counts ----
                label_counts = df["Predicted_Label"].value_counts()

                st.subheader("📌 Predicted Label Distribution")

                # Bar Chart
                fig, ax = plt.subplots(figsize=(6, 4))  # 🔥 Change size here
                ax.bar(label_counts.index, label_counts.values)
                ax.set_xlabel("Labels")
                ax.set_ylabel("Count")
                ax.set_title("Predicted Class Distribution")

                st.pyplot(fig)  

                st.markdown('</div>', unsafe_allow_html=True)

                # =========================================================
                # 🔥 DOWNLOAD PREDICTED FILE
                # =========================================================
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0)

                st.download_button(
                    label="📥 Download Classified Excel",
                    data=buffer,
                    file_name="classified_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


    st.markdown('</div>', unsafe_allow_html=True)
