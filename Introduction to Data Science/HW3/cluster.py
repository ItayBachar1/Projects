
class Cluster:
    def __init__(self, c_id, samples):
        """
         This constructor is the builder of Cluster object
        :param c_id: the id of the cluster
        :param samples: list of samples in the cluster
        """
        self.c_id = c_id
        self.samples = samples

    def merge(self, other):
        """
        Adds the samples from the other cluster to this cluster
        :param other: other cluster to merge with
        """
        self.c_id = min(self.c_id, other.c_id)
        for y in other.samples:
            self.samples.append(y)
        self.samples.sort()

    def print_details(self, silhouette):
        """
        Prints the identifiers of the cluster
        :param silhouette: given silhouette of the cluster
        """
        s_id_list = []
        for sample in self.samples:
            s_id_list.append(sample.s_id)
        s_id_list.sort()
        cluster_number = s_id_list[0]
        dominant_label = self.dominant_label()
        print(f"Cluster ", cluster_number, ":", s_id_list,
              ", dominant label = ", dominant_label, ", silhouette = ", round(silhouette, 3))

    def dominant_label(self):
        """
        Helping function for getting the dominant label in this cluster
        :return: domi_label - the dominant label in this cluster
        """
        label_dict = {"B-CELL_ALL": 0,
                      "B-CELL_ALL_TCF3-PBX1": 0,
                      "B-CELL_ALL_HYPERDIP": 0,
                      "B-CELL_ALL_HYPO": 0,
                      "B-CELL_ALL_MLL": 0,
                      "B-CELL_ALL_T-ALL": 0,
                      "B-CELL_ALL_ETV6-RUNX1": 0}

        max_label = 0
        domi_label = ""
        for sample in self.samples:  # counts the appearance of each label in the cluster
            label_dict[sample.label] += 1
        for key in label_dict.keys():
            if max_label == label_dict[key]:
                sort_list = [domi_label, key]
                sort_list.sort()
                domi_label = sort_list[0]
            if max_label < label_dict[key]:
                domi_label = key
                max_label = label_dict[key]
        return domi_label

    def __lt__(self, other):
        """
        Compares this cluster to other cluster by c_id
        :param other: the other cluster
        :return: if this cluster(c_id) is lower than the other cluster(c_id)
        """
        return self.c_id < other.c_id






