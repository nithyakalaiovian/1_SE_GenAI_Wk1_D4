import streamlit as st

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Beautiful Calculator",
    page_icon="🧮",
    layout="centered"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #334155
    );
}

.main-container {
    max-width: 420px;
    margin: auto;
    padding-top: 40px;
}

.calc-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0px 8px 32px rgba(0,0,0,0.4);
}

.title {
    text-align: center;
    color: white;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 20px;
}

.display {
    background: #0f172a;
    color: #00ffcc;
    font-size: 32px;
    font-weight: bold;
    text-align: right;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    min-height: 70px;
    overflow-x: auto;
}

.stButton > button {
    width: 100%;
    height: 65px;
    border-radius: 15px;
    border: none;
    font-size: 24px;
    font-weight: bold;
    background: rgba(255,255,255,0.12);
    color: white;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #38bdf8;
    transform: scale(1.05);
}

.footer {
    text-align: center;
    color: #cbd5e1;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session State
# ----------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

# ----------------------------
# Functions
# ----------------------------
def add_to_expression(value):
    st.session_state.expression += value

def clear_expression():
    st.session_state.expression = ""

def calculate():
    try:
        result = str(eval(st.session_state.expression))
        st.session_state.expression = result
    except:
        st.session_state.expression = "Error"

# ----------------------------
# UI
# ----------------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">🧮 Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="display">{st.session_state.expression or "0"}</div>',
    unsafe_allow_html=True
)

# Row 1
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("7"):
        add_to_expression("7")

with c2:
    if st.button("8"):
        add_to_expression("8")

with c3:
    if st.button("9"):
        add_to_expression("9")

with c4:
    if st.button("÷"):
        add_to_expression("/")

# Row 2
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("4"):
        add_to_expression("4")

with c2:
    if st.button("5"):
        add_to_expression("5")

with c3:
    if st.button("6"):
        add_to_expression("6")

with c4:
    if st.button("×"):
        add_to_expression("*")

# Row 3
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("1"):
        add_to_expression("1")

with c2:
    if st.button("2"):
        add_to_expression("2")

with c3:
    if st.button("3"):
        add_to_expression("3")

with c4:
    if st.button("−"):
        add_to_expression("-")

# Row 4
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("0"):
        add_to_expression("0")

with c2:
    if st.button("."):
        add_to_expression(".")

with c3:
    if st.button("C"):
        clear_expression()

with c4:
    if st.button("+"):
        add_to_expression("+")

# Row 5
c1, c2 = st.columns([1, 3])

with c1:
    if st.button("("):
        add_to_expression("(")

with c2:
    if st.button("=", use_container_width=True):
        calculate()

c3, c4 = st.columns([1, 1])

with c3:
    if st.button(")"):
        add_to_expression(")")

st.markdown(
    '<div class="footer">Made with ❤️ using Streamlit</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)