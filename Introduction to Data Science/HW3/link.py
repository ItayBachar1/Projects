import abc


class Link:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def compute(self, cluster, other):
        pass


class SingleLink:
    def compute(self, cluster, other):
        """
        compute the distance between given two clusters by single link method
        :param cluster: the first cluster
        :param other: the second cluster
        :return: the distance between given two clusters
        """
        min_distance = cluster.samples[0].compute_euclidean_distance(other.samples[0])
        for sample in cluster.samples:
            for other_sample in other.samples:
                min_distance = min(min_distance, sample.compute_euclidean_distance(other_sample))
        return min_distance


class CompleteLink:
    def compute(self, cluster, other):
        """
        compute the distance between given two clusters by complete link method
        :param cluster: the first cluster
        :param other: the second cluster
        :return: the distance between given two clusters
        """
        max_distance = cluster.samples[0].compute_euclidean_distance(other.samples[0])
        for sample in cluster.samples:
            for other_sample in other.samples:
                max_distance = max(max_distance, sample.compute_euclidean_distance(other_sample))
        return max_distance