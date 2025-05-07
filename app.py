import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("Student Marks Uploader & Downloader")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Check for required column
        if "Total Marks" not in df.columns:
            st.error("❌ The uploaded file must contain a column named 'Total Marks'.")
        else:
            st.success("✅ File successfully loaded!")
            st.dataframe(df)

            # Prepare Excel file for download (.xlsx)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Marks')

            # Download button
            st.download_button(
                label="📥 Download as .xlsx",
                data=output.getvalue(),
                file_name="Processed_Marks.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Please upload an Excel file to begin.")
