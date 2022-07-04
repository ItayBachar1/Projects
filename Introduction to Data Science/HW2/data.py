import pandas


class Data:
    def __init__(self, path):
        """
        This constructor is the builder of Data object
        :parameters: self : Data object, path : the path to the data file
        """
        df = pandas.read_csv(path)
        self.data = df.to_dict(orient="list")  # loading the data to dictionary

    def get_all_districts(self):
        """
        This function return list of all different districts
        :parameters: self : Data object
        :returns: denominazione_region_list : list of different districts
        """
        denominazione_region_list = []
        for i in self.data["denominazione_region"]:
            if i not in denominazione_region_list:  # check if we already insert the i district
                denominazione_region_list.append(i)
        return denominazione_region_list

    def set_districts_data(self, districts):
        """
        This function change the Data object which will contain only the records
        that belongs to the districts in the parm districts
        :parameters: self : Data object, districts : list of districts
        """
        # removing records from last to first to prevent confusion between the indexes after removing records
        reverse_list = []
        for i in self.data["denominazione_region"][::-1]:  # copy the list from last to first
            reverse_list.append(i)
        for index, value in enumerate(reverse_list):
            if value not in districts:  # check if there is a district that not in the given list
                for key in self.data.keys():  # looping all the keys in the data dictionary
                    self.data[key].pop(len(reverse_list)-1-index)  # remove records by his original index