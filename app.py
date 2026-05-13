import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎓 Student Result Analyzer")

subjects = ["Maths", "Science", "English", "Computer", "Social"]

marks = []
for subject in subjects:
    mark = st.number_input(f"Enter marks for {subject}", 0, 100, 0)
    marks.append(mark)

if st.button("Calculate Result"):
    total = sum(marks)
    percentage = total / len(subjects)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    else:
        grade = "Fail"

    st.success(f"Total Marks: {total}")
    st.success(f"Percentage: {percentage:.2f}%")
    st.success(f"Grade: {grade}")

    df = pd.DataFrame({
        "Subject": subjects,
        "Marks": marks
    })

    fig, ax = plt.subplots()
    ax.bar(df["Subject"], df["Marks"])
    st.pyplot(fig)
