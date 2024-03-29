import numpy as np
from sklearn.linear_model import Ridge # RidgeCV
from sklearn.model_selection import KFold, cross_val_score, learning_curve
from sklearn.metrics import  r2_score, mean_squared_error
import matplotlib.pyplot as plt
from joblib import dump

def ridge(X, y, X_train, X_test, y_train, y_test, type_science, encoder, file_name):
    # Create and train the Ridge regression model
    model = Ridge(alpha=1.0)  # Adjust the alpha parameter as needed
    model.fit(X_train, y_train)

    # Make predictions
    y_pred_unrounded = model.predict(X_test)

    y_pred = np.vectorize(lambda x: round(x * 2) / 2)(y_pred_unrounded)

    # evaluate the model performance using mean squred error, root and r squared
    mse = mean_squared_error(y_test, y_pred_unrounded)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred_unrounded)


    y_train_size = y_pred_unrounded.shape[0]
    print("Mean Squared Error (MSE): {:.2f}".format(mse))
    print('Train MSE {:.2f}'.format(mean_squared_error(y_train[:y_train_size], y_pred_unrounded)))
    print('testMSE {:.2f}'.format(mean_squared_error(y_test, y_pred_unrounded)))
    print("Root Mean Squared Error (RMSE): {:.2f}".format(rmse))
    print("R2 score:", r2)

    # this again has an extremely high R2 score, so may be over fit

    # create a kfold to check scores are similar
    kfold = KFold(n_splits=10, shuffle=True, random_state=15)
    scores = cross_val_score(model, X, y, cv=kfold, scoring='r2')
    # the cross-validated scores are very similar, reducing the chance that the model is overfitted
    print('Cross-validation scores:', scores)

    # create a learning curve to see if data is overfitting
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, train_sizes=np.linspace(0.1, 1.0, 10), cv=5)
                                                            
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
                                                            
    plt.plot(train_sizes, train_mean, color='blue', marker='o', markersize=5, label='training score')
    plt.fill_between(train_sizes, train_mean + train_std, train_mean - train_std, alpha=0.15, color='blue')
    plt.plot(train_sizes, test_mean, color='green', linestyle='--', marker='s', markersize=5, label='test score')
    plt.fill_between(train_sizes, test_mean + test_std, test_mean - test_std, alpha=0.15, color='green')
    plt.xlabel('Number of training samples')
    plt.ylabel('Score')
    plt.legend(loc='lower right')
    plt.ylim([0, 1])
    plt.show()
    plt.savefig("model_graphs/" + file_name + "_ridge.png", )
    plt.clf()

    save = input('should it be saved? ')
    if save[0].strip().lower() == 'y':
        if type_science.lower()[0] == 'c':
            dump(model, 'combined_models/combined_ridge.joblib')
            dump(encoder, 'combined_models/combined_ridge_encoding.joblib')
            print('Model save')
        else:
            dump(model, 'triple_models/triple_ridge.joblib')
            dump(encoder, 'triple_models/triple_ridge_encoding.joblib')
            print('Model save')