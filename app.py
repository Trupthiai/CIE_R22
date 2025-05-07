import streamlit as st
import pandas as pd
import io

st.title("🎯 Pharmacy Workshop Marks Calculator")

uploaded_file = st.file_uploader("📤 Upload Excel file with Q1 to Q17", type=["xlsx"])

if uploaded_file:
    try:
        # Read file using openpyxl
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Define columns
        part_a_cols = [f"Q{i}" for i in range(1, 13)]   # Q1–Q12
        part_b_cols = [f"Q{i}" for i in range(13, 18)]  # Q13–Q17

        # Ensure all required columns exist; fill missing with 0
        for col in part_a_cols + part_b_cols:
            if col not in df.columns:
                df[col] = 0

        # ✅ Clamp Part A marks to 0 or 1 only
        df[part_a_cols] = df[part_a_cols].clip(lower=0, upper=1).astype(int)

        # ✅ Clamp Part B marks to 0–6 range
        df[part_b_cols] = df[part_b_cols].clip(lower=0, upper=6)

        # Part A: sum of Q1–Q12
        df["Part A"] = df[part_a_cols].sum(axis=1)

        # Part B: sum of best 3 of Q13–Q17
        df["Part B"] = df[part_b_cols].apply(lambda row: sum(sorted(row.tolist(), reverse=True)[:3]), axis=1)

        # Total Marks = Part A + Part B
        df["Total Marks"] = df["Part A"] + df["Part B"]

        # Round scores to integers for display
        df["Part B"] = df["Part B"].round().astype(int)
        df["Total Marks"] = df["Total Marks"].round().astype(int)

        # Display result
        st.success("✅ Marks calculated successfully!")
        st.dataframe(df)

        # Prepare downloadable Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Scored")

        st.download_button(
            label="📥 Download Final Marks (.xlsx)",
            data=output.getvalue(),
            file_name="Final_Marks.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Upload a valid Excel (.xlsx) file with columns Q1–Q17.")
