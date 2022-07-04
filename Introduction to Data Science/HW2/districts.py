from data import *
import statistics


class Districts:
    def __init__(self, dataset):
        """
        This constructor is the builder of Data object
        :parameters: self : Districts object, dataset : Data object
        """
        self.dataset = dataset  # Data object

    def filter_districts(self, letters):
        """
         This function change dataset(Data object) which will contain only the records
        that the districts name start with the letters in the parm letters
        :parameters: self : Districts object, letters : set of letters
        """
        districts_list = []
        for i in self.dataset.data["denominazione_region"]:  # looping on all districts
            if i[0] in letters:  # check if the first letter is in the given letters set
                districts_list.append(i)  # add the district to districts_list
        self.dataset.set_districts_data(districts_list)  # set the data by the correct districts

    def print_details(self, features, statistic_functions):
        """
        This function prints statistics on data by the features with using the functions in statistic_functions list.
        :parameters: data - dictionary that his keys are the features and the values are lists of the feature's values,
        features - list of features from the data,
        statistic_functions - list of statistic functions from statistics.py
        """
        for feature in features:
            print(feature, end=": ")
            value_of_function = []  # list of the values we want to print
            for function in statistic_functions:
                # add the values after using the functions to the list
                value_of_function.append(function(self.dataset.data[feature]))
            print(f"{value_of_function[0]}, {value_of_function[1]}")

    def determine_day_type(self):
        """
        This function adds "day_type" key to the field data of dataset object,
        the value is list of indicators of 0 and 1 (bad day or good day)
        :parameters: self : Districts object
        """
        day_type_list = []
        # create a list of 1 or 0 by a condition
        for resigned, positive in zip(self.dataset.data["resigned_healed"], self.dataset.data["new_positives"]):
            if resigned - positive > 0:
                day_type_list.append(1)
            else:
                day_type_list.append(0)
        self.dataset.data["day_type"] = day_type_list  # add the list to the key/column "day_type" to the data

    def get_districts_class(self):
        """
        This function returns dictionary that his keys will be all the different districts,
        and his values will be green or not green.
        :parameters: self : Districts object
        :returns: districts_class : dictionary that his keys will be all the different districts,
        and his values will be green or not green.
        """
        districts_class = {}
        all_districts = Data.get_all_districts(self.dataset)  # get all the different districts
        for districts in all_districts:  # set the keys by the different districts and the values by zeros for counting
            districts_class[districts] = 0
        for index, day_type in enumerate(self.dataset.data["day_type"]):
            # count the number of good days for each district
            if day_type == 1:
                districts_class[self.dataset.data["denominazione_region"][index]] += 1
        for districts in all_districts:
            # check if the counting of good days of each district match to green district (over 340 good days)
            if districts_class[districts] > 340:
                districts_class[districts] = "green"
            else:
                districts_class[districts] = "not green"
        return districts_class



