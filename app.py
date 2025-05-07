import streamlit as st
import pandas as pd
import random
import io

st.title("🔁 Generate Q1–Q17 Scores from Total Marks")

uploaded_file = st.file_uploader("📥 Upload Excel file with 'Total Marks' column (max 30)", type=["xlsx"])

if uploaded_file:
    try:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Ensure 'Total Marks' column exists
        if "Total Marks" not in df.columns:
            st.error("❌ Input file must contain a 'Total Marks' column.")
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
                part_a = [1] * part_a_score + [0] * (12 - part_a_score)
                random.shuffle(part_a)
                part_a_dict = {f"Q{i+1}": part_a[i] for i in range(12)}

                # Assign Part B: 3 of Q13–Q17 with total = part_b_score
                part_b_qs = ["Q13", "Q14", "Q15", "Q16", "Q17"]
                selected = random.sample(part_b_qs, 3)
                part_b_dict = {q: 0 for q in part_b_qs}
                remaining = part_b_score

                # Distribute remaining marks for Part B across 3 selected questions
                for q in selected:
                    if remaining == 0:
                        break
                    mark = random.randint(0, min(6, remaining))
                    part_b_dict[q] = mark
                    remaining -= mark

                # Combine all question marks
                all_data = {
                    **part_a_dict,
                    **part_b_dict,
                    "Part A": part_a_score,
                    "Pa
