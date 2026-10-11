from pathlib import Path

import pandas as pd
import streamlit as st

MAX_STUDENTS = 5
TITLE = "Social Eagle - GenAI - Student Performance"
OUTPUT_FILE = "SE_Performance.txt"


def get_grade(mark: float) -> str:
    """Return a grade based on the student's mark."""
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "E"


def build_report(students: list[dict]) -> str:
    """Build a neatly aligned text report, sorted by mark descending."""
    ranked = sorted(students, key=lambda student: student["mark"], reverse=True)
    serial_width, name_width, mark_width, grade_width = 6, 20, 10, 10
    gap = "  "
    columns_width = (
        serial_width + name_width + mark_width + grade_width + len(gap) * 3
    )
    table_width = max(columns_width, len(TITLE))
    summary_width = serial_width + len(gap) + name_width + len(gap)

    lines = [
        "=" * table_width,
        TITLE.upper().center(table_width),
        "=" * table_width,
        (
            f"{'S.NO.':<{serial_width}}{gap}"
            f"{'NAME':<{name_width}}{gap}"
            f"{'MARK':>{mark_width}}{gap}"
            f"{'GRADE':>{grade_width}}"
        ),
        "-" * table_width,
    ]

    for serial_number, student in enumerate(ranked, start=1):
        lines.append(
            f"{serial_number:<{serial_width}}{gap}"
            f"{student['name'].upper():<{name_width}}{gap}"
            f"{student['mark']:>{mark_width}.2f}{gap}"
            f"{student['grade']:>{grade_width}}"
        )

    marks = [student["mark"] for student in ranked]
    lines.extend(
        [
            "-" * table_width,
            f"{'CLASS AVERAGE':<{summary_width}}"
            f"{sum(marks) / len(marks):>{mark_width}.2f}",
            f"{'HIGHEST MARK':<{summary_width}}{max(marks):>{mark_width}.2f}",
            f"{'LOWEST MARK':<{summary_width}}{min(marks):>{mark_width}.2f}",
            "=" * table_width,
        ]
    )

    return "\n".join(lines)


st.set_page_config(
    page_title="Student Performance | Social Eagle",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container {
        max-width: 1100px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
      }
      [data-testid="stMetric"] {
        background: #f6f8fc;
        border: 1px solid #e8edf5;
        padding: 1rem 1.2rem;
        border-radius: 14px;
      }
      .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #eef4ff, #f8f5ff);
        margin-bottom: 1.5rem;
      }
      .hero p {
        color: #596579;
        margin-bottom: 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🦅 Student Performance</h1>
        <p>Enter up to five student records to create a ranked class report.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("student_entry_form"):
    st.subheader("Student records")
    st.caption(
        "Names must contain letters only and be no longer than 20 characters. "
        "Marks must be between 0 and 100."
    )

    entries = []

    header = st.columns([0.15, 0.55, 0.30])
    header[0].markdown("**No.**")
    header[1].markdown("**Student name**")
    header[2].markdown("**Mark**")

    for i in range(MAX_STUDENTS):
        cols = st.columns([0.15, 0.55, 0.30])
        cols[0].markdown(f"**{i + 1}**")

        name = cols[1].text_input(
            "Student name",
            key=f"student_name_{i}",
            label_visibility="collapsed",
            placeholder=f"Student {i + 1} name",
        )
        mark = cols[2].text_input(
            "Mark",
            key=f"student_mark_{i}",
            label_visibility="collapsed",
            placeholder="0–100",
        )
        entries.append((name, mark))

    submitted = st.form_submit_button(
        "Generate performance report",
        type="primary",
        use_container_width=True,
    )

if submitted:
    students = []
    errors = []

    for row_number, (name_text, mark_text) in enumerate(entries, start=1):
        name = name_text.strip()
        mark_text = mark_text.strip()

        # Skip rows where both fields are empty.
        if not name and not mark_text:
            continue

        if not name or not mark_text:
            errors.append(
                f"Row {row_number}: enter both a student name and a mark."
            )
            continue

        if not name.isalpha() or len(name) > 20:
            errors.append(
                f"Row {row_number}: name must contain letters only "
                "and be at most 20 characters."
            )
            continue

        try:
            mark = float(mark_text)
        except ValueError:
            errors.append(f"Row {row_number}: mark must be a number.")
            continue

        if not 0 <= mark <= 100:
            errors.append(
                f"Row {row_number}: mark must be between 0 and 100."
            )
            continue

        students.append(
            {
                "name": name,
                "mark": mark,
                "grade": get_grade(mark),
            }
        )

    if errors:
        for error in errors:
            st.error(error)
        st.session_state.pop("students", None)
        st.session_state.pop("report", None)

    elif not students:
        st.warning("Add at least one complete student record to generate a report.")
        st.session_state.pop("students", None)
        st.session_state.pop("report", None)

    else:
        report = build_report(students)
        ranked_students = sorted(
            students,
            key=lambda student: student["mark"],
            reverse=True,
        )

        st.session_state["students"] = ranked_students
        st.session_state["report"] = report

        # Save a copy on the machine running the Streamlit app.
        Path(OUTPUT_FILE).write_text(report, encoding="utf-8")


if "students" in st.session_state:
    students = st.session_state["students"]
    marks = [student["mark"] for student in students]

    st.divider()
    st.subheader("Class overview")

    metric_cols = st.columns(3)
    metric_cols[0].metric("Students", len(students))
    metric_cols[1].metric("Class average", f"{sum(marks) / len(marks):.2f}")
    metric_cols[2].metric("Top mark", f"{max(marks):.2f}")

    st.subheader("Ranked results")

    results = pd.DataFrame(
        [
            {
                "Rank": index,
                "Student": student["name"],
                "Mark": student["mark"],
                "Grade": student["grade"],
            }
            for index, student in enumerate(students, start=1)
        ]
    )

    st.dataframe(
        results,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Mark": st.column_config.NumberColumn("Mark", format="%.2f"),
        },
    )

    st.subheader("Printable report")
    st.code(st.session_state["report"], language=None)

    st.download_button(
        "Download report as text",
        data=st.session_state["report"],
        file_name=OUTPUT_FILE,
        mime="text/plain",
        type="primary",
    )