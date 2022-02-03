import streamlit as st
import pickle
import numpy as np
import pandas as pd
from feature_cre import extract_features_of_inp_url
from sklearn import svm , preprocessing

def load_module():
    loaded_model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
    st.title("Phishing Url detection applications")
    urL=st.text_input("Enter the url you want to Check")
    #urL ="https://firebasestorage.googleapis.com/v0/b/soav-954b2.appspot.com/o/index.html?alt=media&amp;token=86e7f3e3-fa2c-40fe-a160-fb6e0ac6a956#"#"https://stackoverflow.com/questions/46257627/scikit-learn-preprocessing-scale-vs-preprocessing-standardscalar"
    X = extract_features_of_inp_url(urL)
    X.to_csv("sample.csv",header=None,index=None)
    X = pd.read_csv("sample.csv",header=None,index_col=None)
    print(type(X))
    print(X)
    print(type(X))
    #X = preprocessing.scale(X)
    print(X)
    result = loaded_model.predict(X)
    print("\n PRINTING RESULT")
    print(result)
    if result:
        st.write("url is phishing")
    else:
        st.write("url is legitimate")
    return


#def show_predict_page():
#    st.title("Prediction page for the website")


load_module()
#show_predict_page()









