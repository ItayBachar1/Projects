from data import *
from districts import Districts
from statistics import mean, median
import sys


def main(argv):
    path = argv[1]
    # loading data for each question because the data changes in the first question
    question1_data = Data(path)
    question2_data = Data(path)

    print("Question 1:")
    d_districts = Districts(question1_data)
    letters = {'L', 'S'}
    list_features = ["hospitalized_with_symptoms", "intensive_care", "total_hospitalized", "home_insulation"]
    statistic_functions_list = [mean, median]
    d_districts.filter_districts(letters)  # filter the data by letters set
    # print the statistic functions of the features of the filtered data
    d_districts.print_details(list_features, statistic_functions_list)

    print("\nQuestion 2:")
    print(f"Number of districts:", len(question2_data.get_all_districts()))
    day_type_districts = Districts(question2_data)
    day_type_districts.determine_day_type()  # add the column day_type to data
    count = 0
    # create dictionary of districts with modified the green status
    districts_dict = day_type_districts.get_districts_class()
    for value in districts_dict.values():  # count the not green districts
        if value == "not green":
            count += 1
    print(f"Number of not green districts:", count)
    if count > 10:  # check if the not green districts in Italy are bigger than 10 for forced lockdown
        print(f"Will a lockdown be forced on whole of Italy?:", "Yes")
    else:
        print(f"Will a lockdown be forced on whole of Italy?:", "No")














    # f = Districts(d)
    # g = Data.get_all_districts(d)
    # print(g)
    # Data.set_districts_data(d, ['Abruzzo', 'Basilicata', 'Calabria', 'Campania'])
    # print(d.data["denominazione_region"])
    # Districts.determine_day_type(f)
    # print(f.dataset.data["day_type"])
    # print(f.get_districts_class())



if __name__ == '__main__':
    main(sys.argv)


