def midterm1():
    print('Midterm 1')
    import numpy as np
    import matplotlib.pyplot as plt
    import statistics as stats

    ppl_grades = [8.5, 9.1, 9.5, 8, 7.9, 2.3, 8.8, 9, 10, 1, 9.5, 8.2, 8, 9.8, 8, 7.5, 10, 9.9, 7.8, 9.2]
    ppl_grades_np_array = np.array(ppl_grades)

    # TODO: summary statistics
    print('*** Summary Statistics ***')
    print('range: ', round(np.min(ppl_grades_np_array), 2), '..', round(np.max(ppl_grades_np_array), 2), sep='')
    print('mean:', round(np.average(ppl_grades_np_array), 2))
    print('std:', round(np.std(ppl_grades_np_array), 2), '\n')

    # TODO: boxplot
    q1 = np.quantile(ppl_grades_np_array, .25)
    q3 = np.quantile(ppl_grades_np_array, .75)
    iqr = q3 - q1
    low_outlier_threshold = q1 - (1.5 * iqr)
    high_outlier_threshold = q3 + (1.5 * iqr)

    branches = [ppl_grades_np_array]
    medians = [stats.median(branch) for branch in branches]
    plt.boxplot(
        branches
    )
    branch_labels = []
    i = 0
    for branch in branches:
        max_value = max(branch)
        plt.annotate(str(max_value), xy=(i + 1, max_value))
        plt.annotate(str(medians[i]), xy=(i + 1, medians[i]))
        branch_labels.append('Branch #' + str(i + 1))
        for element in branch:
            if element < low_outlier_threshold or element > high_outlier_threshold:
                plt.annotate(str(element), xy=(i + 1, element))
        i += 1
    axes = plt.gca()
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.set_xticklabels(branch_labels)
    plt.ylabel('PPL Grades - Fall 2021')
    plt.show()
    print('\n\n\n')

midterm1()


def midterm2():
    print('Midterm 2:')
    import pandas as pd

    country_income = [
        ['Ivory Coast', 987],
        ['Panama', 6254],
        ['Zambia', 545],
        ['Colombia', 3259],
        ['Tanzania', 702],
        ['Papua New Guinea', 876],
        ['Georgia', 2273],
        ['Finland', 16332],
        ['Saint Lucia', 4519]
    ]

    df = pd.DataFrame(country_income, columns=['country', 'income'])

    # TODO: compute (and display) income's min and max
    print('Minimum country income: ', df['income'].min(), '(',
          df.loc[df['income'] == df['income'].min(), 'country'].iloc[0], ')')
    print('Maximum country income: ', df['income'].max(), '(',
          df.loc[df['income'] == df['income'].max(), 'country'].iloc[0], ')')

    # TODO: apply min_max normalization to the income column
    normalized_df = df
    normalized_df['income'] = (df['income'] - df['income'].min()) / (df['income'].max() - df['income'].min())
    print('Normalization applied: \n', normalized_df)
    print('\n\n')

    # TODO: sort the dataframe in ascending order of income
    print('Sorting applied: \n', normalized_df.sort_values(by=['income']))

    # print(df)
    '''
    Expected output:
                country    income
    2            Zambia  0.000000
    4          Tanzania  0.009945
    5  Papua New Guinea  0.020967
    0       Ivory Coast  0.027998
    6           Georgia  0.109457
    3          Colombia  0.171914
    8       Saint Lucia  0.251726
    1            Panama  0.361627
    7           Finland  1.000000
    '''
    print('\n\n\n')

midterm2()


def midterm3():
    print('Midterm 3:')
    import pandas as pd
    import random
    from sklearn.tree import DecisionTreeClassifier, export_text

    dataset = [[1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 0, 0, 1, 1], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 0, 0, 1, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1], [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 4],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 0, 1, 0, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 1, 0, 2],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4], [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
               [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 7], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 6, 0, 0, 0, 7],
               [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 4], [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
               [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 1, 0, 2], [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 1, 2],
               [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 6], [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 4, 0, 0, 0, 5],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 4, 0, 0, 0, 5], [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 2, 1, 0, 0, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 2, 0, 1, 1, 1],
               [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 6], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 1, 1], [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 1, 0, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4], [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 6, 0, 1, 0, 6],
               [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 6], [0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 6, 0, 0, 0, 6], [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 6, 0, 0, 0, 7], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 0, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 6],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 4, 1, 0, 0, 5], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 8, 0, 0, 1, 7],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 1, 2], [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 1, 0, 2],
               [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 2, 1, 0, 1, 2], [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 4], [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4],
               [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 3], [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1],
               [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1], [0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 2, 1, 0, 1, 2],
               [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 8, 1, 0, 0, 7], [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4],
               [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1], [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 0, 1, 1],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 3], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 7],
               [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2], [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 3], [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7],
               [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 4], [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 2, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 7],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 4], [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 2, 1, 0, 1, 2],
               [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 6], [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 4, 0, 0, 0, 5],
               [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 4, 1, 0, 1, 3], [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 0, 3],
               [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 4], [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 2, 1, 0, 0, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 2, 1, 0, 1, 2],
               [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 2, 1, 0, 1, 1], [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 6, 0, 0, 0, 6],
               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 1, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7],
               [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 2]]

    df = pd.DataFrame(dataset, columns=['hair', 'feathers', 'eggs', 'milk', 'airbone', 'aquatic', 'predator', 'toothed',
                                        'backbone', 'breathes', 'venomous', 'fins', 'legs', 'tail', 'domestic',
                                        'cat size', 'type'])

    # split the dataset into train and test
    random.seed(1)
    rows_train = random.sample(range(len(df)), k=int(len(df) * .25))
    training_data = pd.DataFrame(columns=df.columns)
    test_data = pd.DataFrame(columns=df.columns)
    for i, row in df.iterrows():
        if i in rows_train:
            training_data = training_data.append(row)
        else:
            test_data = test_data.append(row)

    # train the model
    print('training...')
    X = training_data.iloc[:, 0:-1].values
    Y = training_data.iloc[:,-1].values.astype('int')
    model = DecisionTreeClassifier().fit(X, Y)

    # print the decision tree
    print(export_text(model, feature_names=list(training_data.columns[:-1])))

    # compute and print model accuracy
    correct = 0.0
    for _, row in test_data.iterrows():
        value_predict = model.predict([row[:-1].values])
        if value_predict == row['type']:
            correct += 1.0
    denom = len(test_data.index)
    print('accuracy:', correct / denom)
    print('\n\n\n')

midterm3()