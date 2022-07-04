import math


class Sample:
    def __init__(self, s_id, label, genes):
        """
        This constructor is the builder of Sample object
        :param s_id: the id of the sample
        :param label: the label of the sample
        :param genes: the coordinates of the sample
        """
        self.s_id = s_id
        self.genes = genes
        self.label = label

    def compute_euclidean_distance(self, other):
        """
        compute the distance between two samples by euclidean distance
        :param other: the other sample
        :return: the euclidean distance
        """
        sum_vectors = 0
        for x, y in zip(self.genes, other.genes):
            sum_vectors += pow(x-y, 2)

        return math.sqrt(sum_vectors)

    def __lt__(self, other):
        """
        Compares this sample to other sample by s_id
        :param other: the other sample
        :return: if this sample(s_id) is lower than the other sample(s_id)
        """
        return self.s_id < other.s_id