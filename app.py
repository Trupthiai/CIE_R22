import streamlit as st
import pandas as pd
from io import BytesIO

# Configuration: Questions and distribution weights (sum = 30)
questions = [f'Q{i}' for i in range(1, 18)]
question_weights = [1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 3, 2, 4, 3]

st.title("📊 Distribute Total Marks into Q1–Q17")

uploaded_file = st.file_uploader("Upload Excel with 'Total Marks' column", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        if 'Total Marks' not in df.columns:
            st.error("Excel must have a 'Total Marks' column.")
        else:
            total_weight = sum(question_weights)
            weight_proportions = [w / total_weight for w in question_weights]

            # Distribute marks per student
            distributed_data = []
            for total in df['Total Marks']:
                student_marks = [round(total * p) for p in weight_proportions]
                distributed_data.append(student_marks)

            dist_df = pd.DataFrame(distributed_data, columns=questions)

            # Sum marks question-wise
            question_totals = dist_df.sum()
            grand_total = question_totals.sum()

            # Prepare final DataFrame with just one row of totals + grand total
            result_df = pd.DataFrame([question_totals.tolist()], columns=questions, index=["Total"])
            result_df[30] = grand_total  # Add grand total

            # Show in app
            st.subheader("🧾 Question-wise Totals")
            st.dataframe(result_df)

            # Create downloadable Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                result_df.to_excel(writer, index=False)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Excel",
                data=buffer,
                file_name="Question_Totals_Simplified.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error: {e}")
