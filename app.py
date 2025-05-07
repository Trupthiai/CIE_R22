import streamlit as st
import pandas as pd
import io

# App title
st.title("Student Marks Calculator: Part A (MCQ) + Part B (Descriptive)")

# Upload file
uploaded_file = st.file_uploader("Upload Excel file with Q1 to Q17", type=["xlsx"])

if uploaded_file:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Define question columns
        part_a_cols = [f"Q{i}" for i in range(1, 13)]  # Q1–Q12
        part_b_cols = [f"Q{i}" for i in range(13, 18)] # Q13–Q17

        # Fill missing question columns with 0
        for col in part_a_cols + part_b_cols:
            if col not in df.columns:
                df[col] = 0

        # Compute Part A marks (0–12)
        df["Part A"] = df[part_a_cols].sum(axis=1)

        # Take top 3 highest marks from Part B (Q13–Q17)
        df["Part B"] = df[part_b_cols].apply(lambda row: sorted(row, reverse=True)[:3], axis=1).apply(sum)

        # Compute Total Marks
        df["Total Marks"] = (df["Part A"] + df["Part B"]).round().astype(int)

        # Show data
        st.success("✅ Marks computed successfully.")
        st.dataframe(df)

        # Prepare Excel for download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Scores')

        # Download button
        st.download_button(
            label="📥 Download Final Marks (.xlsx)",
            data=output.getvalue(),
            file_name="Student_Marks_Scored.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Please upload a `.xlsx` file with question columns Q1 to Q17.")
