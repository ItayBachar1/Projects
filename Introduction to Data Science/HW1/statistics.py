from math import ceil


def sum(values):
    """
    This function sum all the values from the list
    :parameters: values - list of numbers
    :returns: sum1 - the final sum of the values
    """
    sum1 = 0
    for i in values:
        sum1 = sum1 + i
    return sum1


def mean(values):
    """
    This function calculates the average of the values
    :parameters: values - list of numbers
    :returns: the final average
    """
    return sum(values) / len(values)


def median(values):
    """
    This function calculates the value that half of the values are smaller or equal to him,
    and the other half of the values are bigger or equal to him.
    :parameters: values - list of numbers
    :returns: the final median
    """
    sort_values = sorted(values)
    # if the number of values is even we calculate the average of the two median values
    if (len(values) % 2) == 0:
        even_median = sort_values[(len(values)//2) - 1] + sort_values[len(values)//2]
        return even_median / 2
    # if the number of values is odd
    else:
        odd_median = ceil((len(values)/2) - 1)
        return sort_values[odd_median]


def population_statistics(feature_description, data, treatment, target, threshold, is_above, statistic_functions):
    """
    This function prints statistics on the data that represent the population
    with using the functions in statistic_functions. The statistic measure on the target feature,
    after gathering the correct records by the following conditions:
    if is_above is true, collect the values in the treatment feature that bigger then threshold,
    else collect the values in the treatment feature that smaller or equal to threshold.
    :parameters: feature_description - string that describe the name of the group,
    data - dictionary that his keys are the features and the values are lists of the feature's values,
    treatment - name of feature from data, target - name of feature from the data,
    threshold - filter value for the feature treatment, is_above - indicator that get true or false,
    statistic_functions - list of statistic functions from statistics.py
    """
    threshold_values = []
    for index, value in enumerate(data[treatment]):
        if is_above:
            if value > threshold:
                threshold_values.append(data[target][index])
        else:
            if value <= threshold:
                threshold_values.append(data[target][index])

    print(f"{feature_description}" ":")
    print(f"{target}:", statistic_functions[0](threshold_values), end=", ")
    statistic_functions.pop(0)
    for func in statistic_functions:
        print(func(threshold_values))






