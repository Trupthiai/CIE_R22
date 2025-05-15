import streamlit as st
import pandas as pd
from io import BytesIO

# Define question levels
levels = ['L1', 'L1', 'L2', 'L1', 'L1', 'L2', 'L1', 'L1', 'L1', 'L1',
          'L2', 'L1', 'L2', 'L3', 'L2', 'L4', 'L3']
questions = [f'Q{i}' for i in range(1, 18)]

st.title("Question Level Summary Generator")

uploaded_file = st.file_uploader("Upload Excel file with Marks", type=["xlsx"])

if uploaded_file:
    # Load the uploaded Excel file
    df = pd.read_excel(uploaded_file)

    try:
        # Compute question totals
        question_totals = df[questions].sum()
        grand_total = question_totals.sum()

        # Prepare output DataFrame
        output_df = pd.DataFrame([levels, questions, question_totals.tolist()],
                                 index=['Level', 'Question', 'Total'])

        output_df[30] = ['', '', grand_total]

        # Display output in the app
        st.subheader("Question-wise Totals Summary")
        st.dataframe(output_df)

        # Create downloadable Excel
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

    except KeyError as e:
        st.error(f"Missing columns in input file: {e}")
