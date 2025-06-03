import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder


def run_model(prediction_data):

    # if the store is closed, sales will be zero
    if (prediction_data["open"] == 0):
        return np.array([0])


    # create dataframe with the data that we receive
    sales_df_original = pd.DataFrame([prediction_data])

    # load data with the historical sales per costumer for each shop
    ID_vs_sales = pd.read_csv('model/store_ID_vs_sales.csv')
    ID_vs_sales.drop(columns=['Unnamed: 0'], inplace=True)

    sales_df = sales_df_original

    #
    # apply one-hot encoding to categorical data
    # 
    # note: since we have only one row in the dataframe, we need to manually specify all possible categories using pd.Categorical,
    # so that pd.get_dummies() generates the full set of expected dummy columns (and we get a df with the same number of columns that our model is expecting)
    #
    sales_df["state_holiday"] = sales_df["state_holiday"].astype(str)
    state_holiday_possible_values = ["0", "a", "b", "c"]
    day_of_week_possible_values = [1,2,3,4,5,6,7]
    encoder = OneHotEncoder(categories=[state_holiday_possible_values, day_of_week_possible_values], drop='first', dtype=int, sparse_output=False)
    encoded = encoder.fit_transform(sales_df[["state_holiday", "day_of_week"]])
    encoded_columns = encoder.get_feature_names_out(["state_holiday", "day_of_week"])
    encoded_columns = [col.replace("day_of_week", "DoW") for col in encoded_columns] # Replace "day_of_week" prefix with "DoW"
    encoded_df = pd.DataFrame(encoded, columns=encoded_columns, index=sales_df.index)

    # Combine df with encoded categorical values with the original dataframe (dropping the original columns)
    sales_df_transformed = pd.concat([
        sales_df.drop(columns=["state_holiday", "day_of_week"]),
        encoded_df
    ], axis=1)

    # convert date to ordinal
    sales_df_transformed["date"] = pd.to_datetime(sales_df_transformed["date"], dayfirst=True).apply(lambda x: x.toordinal())

    # combine the data we receive with the historical data for each store
    sales_df_transformed_boost = pd.merge(left = sales_df_transformed, right= ID_vs_sales, left_on = 'store_ID', right_on = 'store_ID', how='left' )

    # get features
    X = sales_df_transformed_boost.drop(columns = ['store_ID', 'open'])

    # standardize (using the scalar fitted with the training data)
    with open("model/standar_scalation.pkl", "rb") as standard_scalation_file:
        scaler_standard = pickle.load(standard_scalation_file)

    X_standard = scaler_standard.transform(X)

    # load model and make our prediction
    with open("model/XGBRegressor.pkl", "rb") as file:
        xgb_regressor = pickle.load(file)

    y_pred = xgb_regressor.predict(X_standard)

    return y_pred
