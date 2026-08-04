import streamlit as st
import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- LOAD FILES ----------------
model = joblib.load(os.path.join(BASE_DIR, 'employee_model.pkl'))
l1 = joblib.load(os.path.join(BASE_DIR, 'l1.pkl'))
l2 = joblib.load(os.path.join(BASE_DIR, 'l2.pkl'))
l3 = joblib.load(os.path.join(BASE_DIR, 'l3.pkl'))
l4 = joblib.load(os.path.join(BASE_DIR, 'l4.pkl'))
oe = joblib.load(os.path.join(BASE_DIR, 'oe.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))

# ---------------- UI ----------------
st.title("Employee Promotion Prediction")
st.write("Enter Employee Details")

Age = st.number_input("Age", min_value=18, max_value=60, value=30)

Department = st.selectbox(
    "Department",
    ['Sales & Marketing','Operations','Technology','Analytics',
     'R&D','Procurement','Finance','HR','Legal']
)

Education = st.selectbox(
    "Education",
    ["Master's & above", "Bachelor's", "Below Secondary"]
)

Region = st.selectbox(
    "Region",
    ['region_7','region_22','region_19','region_23','region_26','region_2',
     'region_20','region_34','region_1','region_4','region_29','region_31',
     'region_15','region_14','region_11','region_5','region_28','region_17',
     'region_13','region_16','region_25','region_10','region_27','region_30',
     'region_12','region_21','region_8','region_32','region_6','region_33',
     'region_24','region_3','region_9','region_18']
)

Gender = st.selectbox("Gender", ['m','f'])

recruitment_channel = st.selectbox(
    "Recruitment Channel",
    ['sourcing','referred','other']
)

previous_year_rating = st.number_input("Previous Year Rating", min_value=1, max_value=5, value=3)
length_of_service = st.number_input("Length of Service", min_value=1, max_value=40, value=5)
awards_won = st.selectbox("Awards Won", [0, 1])
avg_training_score = st.number_input("Average Training Score", min_value=0, max_value=100, value=60)

# ---------------- PREDICTION ----------------
if st.button("Predict"):

    # Create DataFrame
    input_data = pd.DataFrame({
        'department': [Department],
        'region': [Region],
        'education': [Education],
        'gender': [Gender],
        'recruitment_channel': [recruitment_channel],
        'no_of_trainings': [1],
        'age': [Age],
        'previous_year_rating': [previous_year_rating],
        'length_of_service': [length_of_service],
        'awards_won': [awards_won],
        'avg_training_score': [avg_training_score]
    })

    # Encoding
    input_data['department'] = l1.transform(input_data['department'])
    input_data['region'] = l2.transform(input_data['region'])
    input_data['education'] = oe.transform(input_data[['education']])
    input_data['gender'] = l3.transform(input_data['gender'])
    input_data['recruitment_channel'] = l4.transform(input_data['recruitment_channel'])

    # Scaling
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)

    # Output
    if prediction[0] == 1:
        st.success("Employee will be Promoted 🎉")
    else:
        st.error("Employee will NOT be Promoted ❌")
