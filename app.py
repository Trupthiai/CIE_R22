def distribute_marks(total):
    # Clamp total marks to valid range [0, 30]
    total = max(0, min(30, int(total)))

    # Split into Part A (max 12) and Part B (max 18)
    partA_max = min(12, total)
    partB_max = total - partA_max
    if partB_max > 18:
        partB_max = 18
        partA_max = total - 18

    # --- Part A: Only 1 or blank ---
    a_marks = [''] * 12
    ones_to_assign = min(partA_max, 12)  # Make sure we don't sample more than 12
    if ones_to_assign > 0:
        indices = random.sample(range(12), ones_to_assign)
        for idx in indices:
            a_marks[idx] = 1

    # --- Part B: Choose any 3 of Q13–Q17, max 6 marks each ---
    b_marks = [''] * 5
    selected = random.sample(range(5), 3)
    remaining = partB_max
    for i in selected:
        if remaining <= 0:
            b_marks[i] = ''
        else:
            mark = random.randint(1, min(6, remaining))
            b_marks[i] = mark
            remaining -= mark

    return a_marks + b_marks
