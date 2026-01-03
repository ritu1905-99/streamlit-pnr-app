import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Consolidated Class Analysis", layout="wide")

st.markdown("""
<div style="font-size:40px; font-weight:700; text-align:center; color:#2A4D69;">
📚 Consolidated Classroom Analysis
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("### Upload Multiple Excel Files (Each May Contain Multiple Sheets)")
st.write("Each Sheet = One Class")

uploaded_files = st.file_uploader(
    "Upload Excel Files",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"📄 {len(uploaded_files)} files uploaded")

    consolidated_data = []
    class_counter = 1   # Global class counter across all files

    for file in uploaded_files:
        # Load all sheets from this Excel file
        xls = pd.ExcelFile(file)

        st.markdown(f"### 📘 File: **{file.name}**")
        st.write(f"Contains {len(xls.sheet_names)} sheet(s).")

        for sheet_name in xls.sheet_names:

            df = pd.read_excel(xls, sheet_name=sheet_name)

            if not {"Role", "Utterances", "Predicted_Label"}.issubset(df.columns):
                st.error(f"❌ Sheet '{sheet_name}' does not contain required columns!")
                continue

            # Count each category
            lecture = (df["Predicted_Label"] == "LECT").sum()
            instruction = (df["Predicted_Label"] == "INST").sum()
            question = (df["Predicted_Label"] == "QUES").sum()
            response = (df["Predicted_Label"] == "RESP").sum()

            total = lecture + instruction + question + response

            consolidated_data.append({
                "Speakers": f"Class {class_counter}",
                "Lecture": lecture,
                "Instruction": instruction,
                "Question": question,
                "Response": response,
                "Total": total
            })

            class_counter += 1  # Move to next class number

    # ===========================
    # Final Consolidated DataFrame
    # ===========================
    consolidated_df = pd.DataFrame(consolidated_data)

    st.write("## 📊 Final Consolidated Analysis Sheet")
    st.dataframe(consolidated_df, use_container_width=True)

    # ============= DOWNLOAD BUTTON ==============
    buffer = BytesIO()
    consolidated_df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)

    st.download_button(
        label="📥 Download Consolidated Sheet",
        data=buffer,
        file_name="consolidated_class_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
