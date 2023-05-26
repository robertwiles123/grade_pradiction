import pandas as pd
from joblib import load
import encoding

data = input('What do you want to predict? ')
# clean combined dataframe
combined = pd.read_csv('combined_clean.csv')

# current models I have, though this will be added to and taken away with more data, with accuracy
combined_models_to_predict = ['combined_linear']
combined_models_to_predict_dict = {}

# populate a dict of model with the file so can apply them later as neeeded
for s in combined_models_to_predict:
    model = load(s + '.joblib')
    combined_models_to_predict_dict[s] = model

# check that the dict of files and models are correct
print(combined_models_to_predict_dict)

# for later, can take input of grades if prefered
# data = input('What data do you want to use? If a file, include .csv: ')

if data.endswith('.csv'):
    data = pd.read_csv(data)
# need to see if I can use my own package to do this, not sure it'll fit on this laptop, screen too small


def run_test(data, models=combined_models_to_predict_dict):
    outcomes = {}
    for k, v in combined_models_to_predict_dict.items():
        if isinstance(data, str):
            print('oops')
        # currently does not work, as I do not have enough training data and have missing encoudings. This happens with one shot encouding as well
        elif isinstance(data, pd.DataFrame):
            print(v)
            type = input('Is the dataframe combined or triple? ')
            encoded_data = data.copy()
            combined_data = pd.concat([combined, encoded_data])
            encoded_prediction_data, encoder = encoding.le_science(combined_data, type, train=False, file=True)
            encoded_prediction_data = combined_data[len(combined):]
            encoded_prediction_data = encoded_prediction_data[['Year 10 Combined MOCK GRADE', 'Combined MOCK GRADE term 2']]
            prediction = v.predict(encoded_prediction_data)
            # not able to return encoded data, test file includes data it would have seen 
            outcomes[k] = encoding.le_return(prediction, encoder)
            # being used to check that something is being outputted
            outcomes[k] = prediction

        else:
            print('Neither')
    return outcomes


outcome = run_test(combined)
print(outcome)

# Convert the outcome dictionary to a DataFrame
outcome_df = pd.DataFrame(outcome)

# Join the predicted values with the original DataFrame
predicted_data = data.join(outcome_df)

print(predicted_data)
