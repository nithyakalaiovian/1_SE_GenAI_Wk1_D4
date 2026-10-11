import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️")

st.title("BMI Calculator")
st.write("Enter your height and weight to calculate your BMI.")

height_cm = st.number_input(
    "Enter your height (cm):",
    min_value=1.0,
    value=150.0,
)

weight_kg = st.number_input(
    "Enter your weight (kg):",
    min_value=1.0,
    value=105.0,
)

if st.button("Calculate BMI"):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    st.success(f"Your BMI is: {bmi:.2f}")

    if bmi < 18.5:
        st.warning("You are underweight.")
    elif bmi < 25:
        st.success("You have a normal weight.")
    elif bmi < 30:
        st.warning("You are overweight.")
    else:
        st.error("You are obese.")