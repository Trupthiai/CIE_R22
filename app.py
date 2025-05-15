import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.set_page_config(page_title="Marks Splitter", layout="centered")
st.title("📄 Total Marks Splitter (Part A + Part B)")

st.markdown("""
**📥 Upload Excel File:**  
- Column name must be `Total Marks`  
- Each value should be between **0 and 30**  
- This app splits the marks into:
  - ✅ **Part A (Q1–Q12)**: Max 12 marks → only `1` or blank
  - ✅ **Part B (Q13–Q17)**: Max 18 marks → 3 out of 5 questions, each up to 6 marks  
""")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

questions = [f"Q{i}" for i in range(1, 18)]
partA = questions[:12]  # Q1 to Q12
partB = questions[12:]  # Q13 to Q17

def distribute_marks(total):
    # Clamp total to valid range
    total = max(0, min(30, int(total)))

    # Allocate Part A and Part B marks
    partA_max = min(12, total)
    partB_max = min(18, total - partA_max)

    # Adjust in case total > 30
    if total - partA_max > 18:
        partB_max = 18
        partA_max = total - partB_max

    # --- Part A: assign 1 or blank only ---
    a_marks = [''] * 12
    ones_to_assign = max(0, min(partA_max, 12))
    if ones_to_assign > 0:
        indices = random.sample(range(12), ones_to_assign)
        for idx in indices:
            a_marks[idx] = 1

    # --- Part B: assign to 3 questions randomly ---
    b_marks = [''] * 5
    selected = random.sample(range(5), 3)
    remaining = partB_max
    for i in selected:
        if remaining <= 0:
            break
        mark = random.randint(1, min(6, remaining))
        b_marks[i] = mark
        remaining -= mark

    return a_marks + b_marks

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # Remove whitespace in column names

        if "Total Marks" not in df.columns:
            st.error("❌ Column 'Total Marks' not found in uploaded file.")
        else:
            processed = []
            for val in df["Total Marks"]:
                row = distribute_marks(val)
                processed.append(row)

            output_df = pd.DataFrame(processed, columns=questions)
            output_df["Total Marks"] = df["Total Marks"]

            st.success("✅ Marks distributed successfully!")
            st.dataframe(output_df)

            # Prepare downloadable Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                output_df.to_excel(writer, index=False)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Split Marks Excel",
                data=buffer,
                file_name="Split_Marks_Output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
