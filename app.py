import streamlit as st
import pandas as pd
import numpy as np
import pickle

# pages displayed in the app
app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Churn_Prediction'])

# Home page details
if app_mode == 'Home':
    st.title('Bank Churn Prediction')
    st.markdown('Churn Dataset :')
    data = pd.read_csv('churn.csv')
    drop_cols = ["RowNumber", "CustomerId", "Surname"]
    data.drop(columns=drop_cols, inplace=True)
    st.write(data.head(10))


# Churn Prediction Page details
elif app_mode == 'Churn_Prediction':

    # Prediction page inputs
    st.subheader('Fill in customer details to get prediction')
    st.sidebar.header("Customer Location :")
    geo = {'Geography_France': 1, 'Geography_Germany': 2, 'Geography_Spain': 3}  # Dictionary containing the 3 locations
    CreditScore = st.number_input("CreditScore (300 - 850)", min_value=300, max_value=850)
    Age = st.number_input("Age", min_value=18, step=1)
    Tenure = st.number_input("Tenure", min_value=0, step=1)
    Balance = st.number_input("Balance")
    # NumOfProducts = st.number_input("Number of Products", min_value=1, max_value=4, step=1)
    HasCrCard = st.number_input("Credit Card? (Enter 0 for No and 1 for Yes)", min_value=0, max_value=1, step=1)
    IsActiveMember = st.number_input("Is Member Active? (Enter 0 for No and 1 for Yes)", min_value=0, max_value=1,
                                     step=1)
    EstimatedSalary = st.number_input("Estimated Salary")
    Gender = st.number_input("Gender (Enter 0 for female and 1 for male)", min_value=0, max_value=1, step=1)
    Geography = st.sidebar.radio("Geography", tuple(geo.keys()))  # the .keys() returns a view object containing a
    # list of keys in the geo dictionary

    # If either of the locations is selected [1], the other two remain as [0]
    Geography_France, Geography_Germany, Geography_Spain = 0, 0, 0
    if Geography == 'Geography_France':
        Geography_France = 1
    elif Geography == 'Geography_Germany':
        Geography_Germany = 1
    elif Geography == 'Geography_Spain':
        Geography_Spain = 1

    # Dictionary of our features
    var_dict = {
        'CreditScore': CreditScore,
        'Age ': Age,
        'Tenure': Tenure,
        'Balance': Balance,
        # 'NumOfProducts': NumOfProducts,
        'HasCrCard': HasCrCard,
        'IsActiveMember': IsActiveMember,
        'EstimatedSalary': EstimatedSalary,
        'Gender': Gender,
        'Geography': [Geography_France, Geography_Germany, Geography_Spain],
    }

    # Assign the values of the dictionary to the variable 'features'
    features = [CreditScore, Age, Tenure, Balance, HasCrCard, IsActiveMember, EstimatedSalary,
                Gender, var_dict['Geography'][0], var_dict['Geography'][1], var_dict['Geography'][2]]

    results = np.array(features).reshape(1, -1)

    # Predict button
    if st.button("Predict"):

        file = open("churn_model.pkl", "rb")
        model = pickle.load(file)

        prediction = model.predict(results)
        if prediction[0] == 0:
            st.success('Customer will not churn')
        elif prediction[0] == 1:
            st.error('Customer will churn')
