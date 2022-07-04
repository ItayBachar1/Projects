import sys
from statistics import sum, mean, median, population_statistics
from data import load_data, filter_by_feature, print_details


def main(argv):
    """
     This function is the main function
     :parameters: argv - list of arguments, the first is the path to the main function,
      the second is the path to the csv file, the third is the list of the relevant features.
     """
    path = argv[1]
    # casting the string to list separate by commas
    features = list(argv[2].split(", "))
    data = load_data(path, features)
    relevant_categories = ["hum", "t1", "cnt"]
    list_functions = [sum, mean, median]

    print("Question 1:")

    summer_data, no_summer_data = filter_by_feature(data, "season", {1})
    print("Summer:")
    print_details(summer_data, relevant_categories, list_functions)

    holiday_data, no_holiday_data = filter_by_feature(data, "is_holiday", {1})
    print("Holiday:")
    print_details(holiday_data, relevant_categories, list_functions)

    print("All:")
    print_details(data, relevant_categories, list_functions)

    print()
    print("Question 2:")

    print("if t1<=13.0, then:")

    winter_data, no_winter_data = filter_by_feature(data, "season", {3})
    is_holiday_data, no_holiday_data = filter_by_feature(winter_data, "is_holiday", {1})
    population_statistics("Winter holiday records", is_holiday_data, "t1", "cnt", 13.0, False, [mean, median])
    population_statistics("Winter weekday records", no_holiday_data, "t1", "cnt", 13.0, False, [mean, median])

    print("if t1>13.0, then:")
    population_statistics("Winter holiday records", is_holiday_data, "t1", "cnt", 13.0, True, [mean, median])
    population_statistics("Winter weekday records", no_holiday_data, "t1", "cnt", 13.0, True, [mean, median])


if __name__ == '__main__':
    main(sys.argv)
