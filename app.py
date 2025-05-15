import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import random

st.title("📄 Mark Splitter: Part A & Part B from Total Marks (out of 30)")

uploaded_file = st.file_uploader("Upload Excel with 'Total Marks' column", type=["xlsx"])

questions = [f"Q{i}" for i in range(1, 18)]
partA_questions = [f"Q{i}" for i in range(1, 13)]  # Q1 to Q12
partB_questions = [f"Q{i}" for i in range(13, 18)] # Q13 to Q17

def distribute_marks(total):
    # Split into Part A (max 12) and Part B (max 18)
    partA_max = min(total, 12)
    partB_max = total - partA_max
    if partB_max > 18:
        partB_max = 18
        partA_max = total - 18
    
    # --- Part A ---
    partA_marks = []
    remaining = partA_max
    for _ in range(12):
        if remaining <= 0:
            partA_marks.append('')
        else:
            val = random.choice([0, 1, 2])
            val = min(val, remaining)
            partA_marks.append(val)
            remaining -= val
    
    # --- Part B ---
    partB_marks = [''] * 5
    selected_qs = random.sample(range(5), 3)  # Pick 3 questions to answer
    remaining = partB_max
    for i in selected_qs:
        if remaining <= 0:
            mark = 0
        else:
            mark = random.randint(1, min(6, remaining))
        partB_marks[i] = mark
        remaining -= mark
    
    return partA_marks + partB_marks

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        
        if 'Total Marks' not in df.columns:
            st.error("Input Excel must have a column named 'Total Marks'")
        else:
            output_data = []
            for total in df['Total Marks']:
                distributed = distribute_marks(int(total))
                output_data.append(distributed)

            output_df = pd.DataFrame(output_data, columns=questions)
            st.subheader("📊 Distributed Marks")
            st.dataframe(output_df)

            # Downloadable Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                output_df.to_excel(writer, index=False)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Split Marks Excel",
                data=buffer,
                file_name="Split_Marks_Output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error: {e}")
