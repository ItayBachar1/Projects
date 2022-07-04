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

