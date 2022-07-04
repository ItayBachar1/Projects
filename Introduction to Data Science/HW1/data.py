import pandas


def load_data(path, features):
    """
     This function reads the data from the csv file and load the data to the main memory
     :parameters: path - the path to the csv file, features - list of relevant features that we are interested
     :returns: new_data - the upload data
     """
    df = pandas.read_csv(path)
    data = df.to_dict(orient="list")
    # filter the data by relevant features
    new_data = {}
    for feature in features:
        new_data[feature] = data[feature]
    return new_data


def filter_by_feature(data, feature, values):
    """
     This function separate the data to two data by values of the feature
     that in the value's set or not in the value's set.
     :parameters: data - dictionary that his keys are the features and the values are lists of the feature's values,
     feature - name of categorical feature,
     values - set of values that the feature can fill the values.
     :returns: data1 - the data with the relevant values, data2 - the data without the relevant values.
     """
    # creates the items of dictionaries
    data1 = {}
    data1["cnt"] = []
    data1["t1"] = []
    data1["hum"] = []
    data1["season"] = []
    data1["is_holiday"] = []
    data2 = {}
    data2["cnt"] = []
    data2["t1"] = []
    data2["hum"] = []
    data2["season"] = []
    data2["is_holiday"] = []
    for index, value in enumerate(data[feature]):
        if value in values:
            data1["cnt"].append(data["cnt"][index])
            data1["t1"].append(data["t1"][index])
            data1["hum"].append(data["hum"][index])
            data1["season"].append(data["season"][index])
            data1["is_holiday"].append(data["is_holiday"][index])
        else:
            data2["cnt"].append(data["cnt"][index])
            data2["t1"].append(data["t1"][index])
            data2["hum"].append(data["hum"][index])
            data2["season"].append(data["season"][index])
            data2["is_holiday"].append(data["is_holiday"][index])

    return data1, data2


def print_details(data, features, statistic_functions):
    """
     This function prints statistics on data only by the features with using the functions in statistic_functions list.
     :parameters: data - dictionary that his keys are the features and the values are lists of the feature's values,
     features - list of features from the data,
     statistic_functions - list of statistic functions from statistics.py
     """
    for feature in features:
        print(feature, end=": ")
        # list of the values we want to print
        value_of_function = []
        for function in statistic_functions:
            value_of_function.append(function(data[feature]))
        print(f"{value_of_function[0]}, {value_of_function[1]}, {value_of_function[2]}")
