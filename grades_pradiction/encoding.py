# at some point this needs to be returned to grades_packages, but was having issues with the installing and for now would rather work on the models
from sklearn.preprocessing import LabelEncoder

def le_science(dataframe, type, train=True, file=False):
    learning_grades = dataframe.copy()
    if type.lower()[0] == 'c':
        columns_to_encode = ['Year 10 Combined MOCK GRADE', 'Combined MOCK GRADE term 2', 'Combined MOCK GRADE Term 4']
        le = LabelEncoder()
        for col in columns_to_encode:
            learning_grades[col] = le.fit_transform(dataframe[col])
        if train:
            X = learning_grades[['Year 10 Combined MOCK GRADE', 'Combined MOCK GRADE term 2']]
            y = learning_grades['Combined MOCK GRADE Term 4']
    elif type.lower([0]) == 't':
        columns_to_encode = ['FFT20', 'year 10 bio grade', 'year 10 chem grade', 'year 10 phys grade', 
                            'year 11 paper 1 bio grade', 'year 11 paper 1 chem grade', 'year 11 paper 1 phys grade',
                            'year 11 paper 2 bio grade', 'year 11 paper 2 chem grade', 'year 11 paper 2 phys grade']
        for col in columns_to_encode:
            learning_grades[col] = le.fit_transform(dataframe[col])
        if train:
            X = learning_grades[['year 10 bio grade', 'year 10 chem grade', 'year 10 phys grade', 
                            'year 11 paper 1 bio grade', 'year 11 paper 1 chem grade', 'year 11 paper 1 phys grade']]
            y = learning_grades[['year 11 paper 2 bio grade', 'year 11 paper 2 chem grade', 'year 11 paper 2 phys grade']]
    else:
        print('Neither science selected')
    if train:
        if not file:
            return learning_grades, X, y
        else:
            return learning_grades, X, y, le

    else:
        if not file:
            return learning_grades
        else:
            return learning_grades, le

def le_return(data, le):
    return le.inverse_transform(data)