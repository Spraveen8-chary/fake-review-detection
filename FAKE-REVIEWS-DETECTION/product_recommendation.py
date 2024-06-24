from joblib import load
import numpy as np
import pandas as pd
import data

loaded_U, loaded_sigma, loaded_Vt = load('svd_model.joblib')

loaded_pivot_df = load('pivot_df.joblib')

loaded_preds_df = load('preds_df.joblib')

def predict_for_user(user_id,num_recommendations = 100, U=loaded_U, sigma=loaded_sigma, Vt=loaded_Vt, pivot_df=loaded_pivot_df):
    user_idx = user_id - 1

    # Calculate the predicted ratings for the user
    user_predictions = np.dot(np.dot(U[user_idx, :], sigma), Vt)
    # print(user_predictions)
    # Create a DataFrame with the product IDs and predicted ratings
    predictions_df = pd.DataFrame({'ProductID': pivot_df.columns, 'PredictedRating': user_predictions})

    # Sort the DataFrame by predicted ratings in descending order
    predictions_df = predictions_df.sort_values(by='PredictedRating', ascending=False)

    # Display the top recommendations for the user
    top_recommendations = predictions_df.head(num_recommendations)
    return top_recommendations


# print(list(predictions.ProductID))
# print(len(loaded_pivot_df.columns))
products = data.products
ids = data.ids

# result = []
def find_product_by_id(products, ids, target_id):
    global result
    result = []
    for product, product_id in zip(products, ids):
        if product_id == target_id:
            # print(product)
            result.append(product)
            return product
    print("NONE")
    return "None"


count = 0

def recommends(r):
    global count
    
    if count % 5 == 0:
        print(r[count:count + 5])
    count += 5



if __name__ == '__main__':
    # Example: Make predictions for a specific user
    user_id_to_predict = 5

    predictions = predict_for_user(user_id_to_predict)

    print(f"Top {100} recommendations for User {user_id_to_predict}:\n", predictions)

    r = []
    for i in list(predictions.ProductID):
        r.append(find_product_by_id(target_id=i,products=products,ids= ids))
    print(r)
    click = 0
    while click<20:
        recommends(r)
        click+=1

