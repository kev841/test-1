import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("notebook/diabetes.pkl", "rb"))

st.title("Diabetes Risk Dashboard")

# Session state to store multiple entries
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Patient", "Probability", "Risk"])

# Side-by-side input and result
col1, col2 = st.columns(2)

with col1:
    st.header("Patient Data")
    patient_name = st.text_input("Patient Name", "Patient 1")
    pregnancies = st.slider("Pregnancies", 0, 20, 0)
    glucose = st.slider("Glucose Level", 50, 200, 100)
    blood_pressure = st.slider("Blood Pressure", 60, 140, 80)
    skin_thickness = st.slider("Skin Thickness", 0, 100, 20)
    insulin = st.slider("Insulin", 0, 300, 80)
    bmi = st.slider("BMI", 10.0, 50.0, 25.0)
    dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
    age = st.slider("Age", 10, 100, 30)
    
    if st.button("Predict & Add to Dashboard"):
        # Prepare input
        input_df = pd.DataFrame({
            "Pregnancies": [pregnancies],
            "Glucose": [glucose],
            "BloodPressure": [blood_pressure],
            "SkinThickness": [skin_thickness],
            "Insulin": [insulin],
            "BMI": [bmi],
            "DiabetesPedigreeFunction": [dpf],
            "Age": [age]
        })
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        risk = "High" if prediction == 1 else "Low"
        
        # Add to history
        st.session_state.history.loc[len(st.session_state.history)] = [patient_name, probability, risk]

with col2:
    st.header("Prediction Result")
    if st.session_state.history.empty:
        st.info("Enter patient data and click 'Predict & Add to Dashboard'")
    else:
        last_entry = st.session_state.history.iloc[-1]
        st.subheader(f"{last_entry['Patient']}")
        st.bar_chart([1 - last_entry["Probability"], last_entry["Probability"]], use_container_width=True)
        color = "green" if last_entry["Risk"] == "Low" else "red"
        st.markdown(f"<h2 style='color:{color}'>{last_entry['Risk']} Risk</h2>", unsafe_allow_html=True)
    
    st.subheader("Dashboard")
    if not st.session_state.history.empty:
        st.dataframe(st.session_state.history)
        # Plot all probabilities
        st.line_chart(st.session_state.history["Probability"])