import pandas
from sample import *


class Data:
    def __init__(self, path):
        """
        This constructor is the builder of Data object
        :parameters: self : Data object, path : the path to the data file
        """
        df = pandas.read_csv(path)
        self.data = df.to_dict(orient="list")  # loading the data to dictionary

    def create_samples(self):
        """
        Creating list of Sample objects from the given data.
        :return: samples_list - list of Sample objects
        """
        samples_list = []
        for index in range(len(self.data['samples'])):
            genes_list = []
            for key in self.data.keys():  # adds the genes of the samples
                if key != 'samples' and key != 'type':
                    genes_list.append(self.data[key][index])
            # adds the s_id and the label of the samples
            sample = Sample(self.data['samples'][index], self.data['type'][index], genes_list)
            samples_list.append(sample)
        return samples_list