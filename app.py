import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("Student Marks Uploader & Downloader")

# File uploader
uploaded_file = st.file_uploader("Upload Excel File (.xlsx or .xls)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)
        
        # Check if the "Total Marks" column exists
        if "Total Marks" not in df.columns:
            st.error("❌ The uploaded file must contain a column named 'Total Marks'.")
        else:
            st.success("✅ File successfully loaded!")
            st.dataframe(df)

            # Allow the user to download the modified file as .xls
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlwt') as writer:
                df.to_excel(writer, index=False, sheet_name='Marks')

            # Download button
            st.download_button(
                label="📥 Download as .xls",
                data=output.getvalue(),
                file_name="Processed_Marks.xls",
                mime="application/vnd.ms-excel"
            )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Please upload an Excel file to begin.")
