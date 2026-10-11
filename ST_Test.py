import streamlit as st

st.set_page_config(page_title="Calculator", page_icon="🧮")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at top left, #e9f2ff 0%, transparent 55%),
            linear-gradient(135deg, #f8faff, #edf3fc);
    }

    /* Faint maths symbols behind the app content */
    .stApp::before {
        content: "＋     ∑       √       π       ÷       ∫       ×       ∞       −       θ       ＝       Δ";
        position: fixed;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 30px;
        color: #54739b;
        opacity: 0.07;
        font-size: clamp(30px, 5vw, 70px);
        line-height: 2.5;
        letter-spacing: 18px;
        text-align: center;
        word-spacing: 30px;
        transform: rotate(-12deg) scale(1.2);
        pointer-events: none;
        z-index: 0;
    }

    /* Keep the calculator content above the background */
    .stApp > header,
    .stApp [data-testid="stAppViewContainer"] {
        position: relative;
        z-index: 1;
    }

    h1 {
        color: #173b68;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧮 Calculator")
st.write("Enter two numbers and choose an operator.")

a = st.number_input("Enter the first number:", value=0.0)
operator = st.selectbox(
    "Select an operator:",
    ["add", "subtract", "multiply", "divide"],
)
b = st.number_input("Enter the second number:", value=0.0)

if st.button("Calculate"):
    if operator == "add":
        result = a + b
    elif operator == "subtract":
        result = a - b
    elif operator == "multiply":
        result = a * b
    elif operator == "divide":
        if b == 0:
            st.error("Cannot divide by zero.")
            result = None
        else:
            result = a / b

    if result is not None:
        st.success(f"The result is: {result}")