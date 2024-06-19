# Importing Dependencies
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
import joblib

def main():
    credit = pd.read_csv('credit approval.csv')

    # Replace "?" with NaN
    credit.replace('?', np.NaN, inplace = True)

    # Convert Age to numeric
    credit["Age"] = pd.to_numeric(credit["Age"])

    #replace missing values with mean values of numeric columns
    credit["Age"].fillna(credit["Age"].mean(), inplace=True)
    credit["ZipCode"].fillna(credit["ZipCode"].mean(), inplace=True)
    credit_drop=credit.drop(["ZipCode"],axis=1)

    credit["Gender"]= credit["Gender"].fillna(credit["Gender"].mode().iloc[0])
    credit["Married"] = credit["Married"].fillna(credit["Married"].mode().iloc[0])
    credit["BankCustomer"]= credit["BankCustomer"].fillna(credit["BankCustomer"].mode().iloc[0])
    credit["EducationLevel"] = credit["EducationLevel"].fillna(credit["EducationLevel"].mode().iloc[0])
    credit["Ethnicity"] = credit["Ethnicity"].fillna(credit["Ethnicity"].mode().iloc[0])

    credit_drop = credit
    credit_drop = credit.drop(["ZipCode"],axis=1)

    # Label Encoder
    LE = LabelEncoder()
    #Using label encoder to convert into numeric types
    for col in credit_drop:
        if credit_drop[col].dtypes=='object':
            credit_drop[col]=LE.fit_transform(credit_drop[col])

    #convert to categorical data to dummy data
    credit_dummies = pd.get_dummies(credit_drop, columns=[ "Married","EducationLevel", "Citizen", "DriversLicense", "Ethnicity"])

    credit_dummies.to_numpy

    X,y = credit_dummies.iloc[:,credit_dummies.columns != 'Approved'] , credit_dummies["Approved"]

    # Spliting the data into training and testing sets
    X_train, X_test, y_train, Y_test = train_test_split(X,
                                    y,
                                    test_size=0.2,
                                    random_state=123)

    # Scaling X_train and X_test
    scaler = MinMaxScaler(feature_range=(0, 1))
    rescaledX_train = scaler.fit_transform(X_train)
    rescaledX_test = scaler.transform(X_test)
    rescaledX = scaler.transform(X)
    #decision trees
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)


    filename = "Decision_Tree_Model.pkl"
    #Save model
    joblib.dump(clf, filename)

    #load model
    loaded_model = joblib.load(filename)
    

if __name__ == '__main__':
    main()