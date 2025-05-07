import streamlit as st
import pandas as pd
import numpy as np
import random
import io

st.title("🔁 Generate Q1–Q17 Scores from Total Marks")

uploaded_file = st.file_uploader("📥 Upload Excel file with 'Total Marks' column (max 30)", type=["xlsx"])

if uploaded_file:
    try:
        # Load data
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        if "Total Marks" not in df.columns:
            st.error("❌ Input file must have a 'Total Marks' column.")
        else:
            def distribute_marks(total):
                # Clamp total between 0–30
                total = max(0, min(30, int(total)))

                # Randomly assign Part A (0–12), rest to Part B (max 18)
                max_part_a = min(12, total)
                min_part_a = max(0, total - 18)
                part_a_score = random.randint(min_part_a, max_part_a)
                part_b_score = total - part_a_score

                # Assign Part A marks (Q1–Q12), each 0 or 1, summing to part_a_score
                part_a = [1]*part_a_score + [0]*(12 - part_a_score)
                random.shuffle(part_a)

                # Assign Part B: Pick 3 questions from Q13–Q17 and assign marks summing to part_b_score
                part_b_qs = ["Q13", "Q14", "Q15", "Q16", "Q17"]
                selected_qs = random.sample(part_b_qs, 3)
                part_b = {q: 0 for q in part_b_qs}

                # Distribute part_b_score across 3 questions (max 6 each)
                remain = part_b_score
                for q in selected_qs:
                    if remain == 0:
                        break
                    mark = random.randint(0, min(6, remain))
                    part_b[q] = mark
                    remain -= mark

                # Fill Part A Q1–Q12
                part_a_dict = {f"Q{i+1}": mark for i, mark in enumerate(part_a)}

                # Merge all question marks
                all_questions = {**part_a_dict, **part_b}
                all_questions["Part A"] = part_a_score
                all_questions["Part B"] = part_b_score
                all_questions["Total Marks"] = total

                return pd.Series(all_questions)

            # Apply distribution logic
            results = df["Total Marks"].apply(distribute_marks)
            final_df = pd.concat([df, results], axis=1)

            # Display
            st.success("✅ Scores generated successfully!")
            st.dataframe(final_df)

            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False, sheet_name="Generated")

            st.download_button(
                label="📥 Download Q1–Q17 File (.xlsx)",
                data=output.getvalue(),
                file_name="Generated_Q_Scores.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Upload a `.xlsx` file with only a 'Total Marks' column.")
