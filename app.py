import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.title("📄 Total Marks Splitter (Part A + Part B)")

st.markdown("""
**Input Format:** Excel file with a column named **`Total Marks`**  
- **Part A (Q1–Q12)**: Max 12 marks → each question = 0, 1, or blank  
- **Part B (Q13–Q17)**: Max 18 marks → any 3 out of 5 questions answered, each up to 6 marks  
""")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

questions = [f"Q{i}" for i in range(1, 18)]
partA = questions[:12]  # Q1–Q12
partB = questions[12:]  # Q13–Q17

def distribute_marks(total):
    # Split total into Part A and Part B
    partA_max = min(12, total)
    partB_max = total - partA_max
    if partB_max > 18:
        partB_max = 18
        partA_max = total - 18

    # --- Part A Distribution (Q1–Q12): Only 0, 1, or blank ---
    a_marks = []
    remaining = partA_max
    for _ in range(12):
        if remaining <= 0:
            a_marks.append('')
        else:
            mark = random.choice([0, 1])
            mark = min(mark, remaining)
            a_marks.append(mark)
            remaining -= mark

    # --- Part B Distribution (Q13–Q17): Only 3 questions attempted, max 6 each ---
    b_marks = [''] * 5
    selected = random.sample(range(5), 3)
    remaining = partB_max
    for i in selected:
        if remaining <= 0:
            b_marks[i] = 0
        else:
            mark = random.randint(1, min(6, remaining))
            b_marks[i] = mark
            remaining -= mark

    return a_marks + b_marks

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        if "Total Marks" not in df.columns:
            st.error("❌ 'Total Marks' column not found in uploaded file.")
        else:
            data = []
            for total in df["Total Marks"]:
                total = int(total)
                row = distribute_marks(total)
                data.append(row)

            result_df = pd.DataFrame(data, columns=questions)
            result_df["Total Marks"] = df["Total Marks"]

            st.success("✅ Marks distributed successfully!")
            st.dataframe(result_df)

            # Downloadable Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                result_df.to_excel(writer, index=False)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Output Excel",
                data=buffer,
                file_name="Split_Marks_Output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error: {e}")
