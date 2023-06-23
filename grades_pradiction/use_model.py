import pandas as pd
from joblib import load
import encoding
import df_columns

data = input('What do you want to predict? ')
# clean combined dataframe
type = input('Is the data for combined or triple? ')

# current models I have, though this will be added to and taken away with more data, with accuracy
if type.lower()[0] == 'c':
    combined_models_to_predict = ['combined_linear', 'combined_random_forest', 'combined_descition_tree']
    combined_models_to_predict_dict = {}
    for s in combined_models_to_predict:
        model = load(s + '.joblib')
        combined_models_to_predict_dict[s] = model
    # check that the dict of files and models are correct
    print(combined_models_to_predict_dict)
elif type.lower()[0] == 't':
    tripe_models_to_predict = ['triple_linear', 'triple_random_forest', 'triple_descition_tree']
    triple_models_to_predict_dict = {}
    # populate a dict of model with the file so can apply them later as neeeded
    for s in tripe_models_to_predict:
        model = load(s + '.joblib')
        triple_models_to_predict_dict[s] = model
        # check that the dict of files and models are correct
    print(triple_models_to_predict_dict)
else:
    print('Failed to detarmine, no model loaded')
    

if data.endswith('.csv'):
    data = pd.read_csv(data)


outcomes = {}
if type.lower()[0] == 'c':
    for k, v in combined_models_to_predict_dict.items():
        # currently does not work, as I do not have enough training data and have missing encoudings. This happens with one shot encouding as well
        if isinstance(data, str):
            print('oops')
        elif isinstance(data, pd.DataFrame):
                encoder = load(k + '_encoding.joblib')
                encoded_data = encoding.new_data_one_hot(data, encoder)
                prediction = v.predict(encoded_data)
                pred_df = pd.DataFrame({k+'_predicted grades': prediction})
                outcomes[k] = prediction
        else:
                print('Error')
    df_with_predictions = data.assign(**outcomes)
    columns_to_skip = df_columns.combined_columns()
    for column in df_with_predictions.columns:
        if column not in columns_to_skip:
            df_with_predictions[column] = df_with_predictions[column].apply(lambda x: round(x * 2) / 2)

    print(df_with_predictions)
elif type.lower()[0] == 't':
    outcome_df = pd.DataFrame()
    for k, v in triple_models_to_predict_dict.items():
        # currently does not work, as I do not have enough training data and have missing encoudings. This happens with one shot encouding as well
        if isinstance(data, str):
            print('oops')
        elif isinstance(data, pd.DataFrame):
        # Doesn't work, probably because 3 numpy array at a guess
                encoder = load(k + '_encoding.joblib')
                encoded_data = encoding.new_data_one_hot(data, encoder)
                prediction = v.predict(encoded_data)
                outcomes[k] = prediction
    for key, values in outcomes.items():
        for i, value in enumerate(values):
            column_name = f"{key}_{i+1}"
            outcome_df[column_name] = value
        else:
            print('error')
         

