import streamlit as st
import pandas as pd
from io import BytesIO

# Define question levels and corresponding questions
levels = ['L1', 'L1', 'L2', 'L1', 'L1', 'L2', 'L1', 'L1', 'L1', 'L1',
          'L2', 'L1', 'L2', 'L3', 'L2', 'L4', 'L3']
questions = [f'Q{i}' for i in range(1, 18)]

st.title("📊 Question Level Summary Generator")

uploaded_file = st.file_uploader("Upload Excel file with Marks (Q1 to Q17)", type=["xlsx"])

if uploaded_file:
    try:
        # Load and clean the Excel file
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces

        # Drop unnamed columns if present
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Check if all required questions are in the DataFrame
        missing_cols = [q for q in questions if q not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
        else:
            # Compute totals
            question_totals = df[questions].sum()
            grand_total = question_totals.sum()

            # Prepare output DataFrame
            output_df = pd.DataFrame([levels, questions, question_totals.tolist()],
                                     index=['Level', 'Question', 'Total'])

            output_df[30] = ['', '', grand_total]

            # Show summary
            st.subheader("📋 Question-wise Totals Summary")
            st.dataframe(output_df)

            # Excel download
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                output_df.to_excel(writer, index=True, header=False)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Summary as Excel",
                data=buffer,
                file_name="Question_Level_Summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")
