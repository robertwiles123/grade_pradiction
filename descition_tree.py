import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score, learning_curve
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from grades_packages import encoding
from joblib import dump
# from sklearn.model_selection import GridSearchCV

file_name = input('What file do you want to test? ')
learning_grades = pd.read_csv('csv_clean/' + file_name + '.csv')

type_science = input('Is it triple or combined? ')

encoder, X, y = encoding.one_hot_fit(learning_grades, type_science)
"""
dt = DecisionTreeRegressor()

param_grid = {
    'max_depth': [3, 5, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'random_state': [142]
}

# Create the GridSearchCV object
grid_search = GridSearchCV(dt, param_grid, cv=5)

# Perform grid search on the dataset
grid_search.fit(X, y)

# Print the best parameters and best score found during grid search
print("Best Parameters: ", grid_search.best_params_)
print("Best Score: ", grid_search.best_score_)
"""

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

if type_science.lower()[0] == 'c':
    dtr = DecisionTreeRegressor(random_state=142, max_depth=None, min_samples_leaf=1, min_samples_split=5)
elif type_science.lower()[0] == 't':
    dtr = DecisionTreeRegressor(random_state=142, max_depth=3, min_samples_leaf=2, min_samples_split=10)
else:
    print('No model loaded')

dtr.fit(X_test, y_test)

y_pred_unrounded = dtr.predict(X_test)

y_pred = np.vectorize(lambda x: round(x * 2) / 2)(y_pred_unrounded)

y_train_size = y_pred.shape[0]
mse = mean_squared_error(y_test, y_pred)
print('Train MSE {:.2f}'.format(mean_squared_error(y_train[:y_train_size], y_pred)))
print('test MSE {:.2f}'.format(mean_squared_error(y_test, y_pred)))
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print('Mean Squared Error (MSE):', mse)
print('Root Mean Squared Error (RMSE):', rmse)
print('R2 Score:', r2)

# to check for overfitting

kfold = KFold(n_splits=10, shuffle=True, random_state=15)
scores = cross_val_score(dtr, X, y, cv=kfold, scoring='r2')
# the cross-validated scores are very similar, reducing the chance that the model is overfitted
print('Cross-validation scores:', scores)

train_sizes, train_scores, test_scores = learning_curve(dtr, X, y, train_sizes=np.linspace(0.1, 1.0, 10), cv=5)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.plot(train_sizes, train_mean, color='blue', marker='o', markersize=5, label='training score')
plt.fill_between(train_sizes, train_mean + train_std, train_mean - train_std, alpha=0.15, color='blue')
plt.plot(train_sizes, test_mean, color='green', linestyle='--', marker='s', markersize=5, label='test score')
plt.fill_between(train_sizes, test_mean + test_std, test_mean - test_std, alpha=0.15, color='green')
plt.xlabel('Number of training samples')
plt.xscale('log')
plt.ylabel('Score')
plt.legend(loc='lower right')
plt.show()
plt.savefig("model_graphs/" + file_name + "_descition.png", )

save = input('should it be saved? ')
if save[0].strip().lower() == 'y':
    if type_science.lower()[0] == 'c':
        dump(dtr, 'combined_models/combined_descition_tree.joblib')
        dump(encoder, 'combined_models/combined_descition_tree_encoding.joblib')
        print('Model save')
    else:
        dump(dtr, 'triple_models/triple_descition_tree.joblib')
        dump(encoder, 'triple_models/triple_descition_tree_encoding.joblib')
        print('Model save')
