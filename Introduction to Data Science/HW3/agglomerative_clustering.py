import cluster


class AgglomerativeClustering:
    def __init__(self, link, samples):
        """
        This constructor is the builder of AgglomerativeClustering object
        :param link: the method of calculating the distance between two clusters
        :param samples: the samples of the all data
        """
        self.link = link
        self.samples = samples
        self.clusters = []

    def sample_sil(self, sample, cluster):
        """
        calculates silhouette of given sample
        :param sample: the given sample
        :param cluster: the cluster that the given sample belong to
        :return: the silhouette
        """
        in_sample = self.in_silhouette(sample, cluster)
        out_sample = self.out_silhouette(sample, cluster)
        return (out_sample - in_sample) / max(in_sample, out_sample)

    def compute_silhouette(self):
        """
        computed silhouette of each sample in the data
        :return: dictionary of samples keys with silhouette values
        """
        sil_dict = {}
        for clust in self.clusters:
            for sample in clust.samples:
                if len(clust.samples) > 1:
                    sil_dict[sample.s_id] = self.sample_sil(sample, clust)
                else:
                    sil_dict[sample.s_id] = 0
        return sil_dict

    def compute_summery_silhouette(self):
        """
        computed silhouette of each cluster in the data
        :return: dictionary of clusters keys with silhouette values
        """
        clusters_dict = {}
        sum_of_all_samples = 0
        sum_sil_dict = self.compute_silhouette()
        for clust in self.clusters:
            sum_samples_in_cluster = 0
            for sample in clust.samples:
                sum_of_all_samples += sum_sil_dict[sample.s_id]
                sum_samples_in_cluster += sum_sil_dict[sample.s_id]
            clusters_dict[clust.c_id] = sum_samples_in_cluster / len(clust.samples)
        clusters_dict[0] = sum_of_all_samples / len(self.samples)  # the silhouette value of the data
        return clusters_dict

    def in_silhouette(self, sample, cluster):
        """
        calculates the average distance from sample to each sample in his cluster
        :param sample: the given sample
        :param cluster: the cluster of the sample
        :return: the in rank of the given sample
        """
        sum_dist = 0
        in_sample = 0
        for other_sample in cluster.samples:
            if sample.s_id != other_sample.s_id:
                sum_dist += sample.compute_euclidean_distance(other_sample)
                if len(cluster.samples) > 1:
                    in_sample = (sum_dist / (len(cluster.samples)-1))
                else:
                    in_sample = 0
        return in_sample

    def out_silhouette(self, sample, cluster):
        """
        calculates the min average distance from sample to each sample in other cluster
        :param sample: the given sample
        :param cluster: the cluster of the sample
        :return: the out rank of the given sample
        """
        average = []  # list of the average distance from sample to each sample in other cluster
        for other_cluster in self.clusters:
            sum_dist = 0
            if cluster.c_id != other_cluster.c_id:
                for other_sample in other_cluster.samples:
                    sum_dist += sample.compute_euclidean_distance(other_sample)
                average.append(sum_dist/len(other_cluster.samples))
        out_sample = min(average)
        return out_sample

    def compute_rand_index(self):
        """
        computes the accuracy by the right predictions from the all predictions of the algorithm
        :return: the rand index value
        """
        tp = 0
        tn = 0
        for sample in self.samples:
            for sample1 in self.samples:
                if sample != sample1:
                    if self.predict_label(sample) == self.predict_label(sample1):
                        if sample.label == sample1.label:
                            tp += 1
                    elif sample.label != sample1.label:
                        tn += 1
        return ((tp + tn) / 2) / ((len(self.samples)*(len(self.samples)-1)) / 2)

    def predict_label(self, sample):
        """
        the label that the given sample belongs to
        :param sample: the given sample
        :return: the cluster id of the sample
        """
        for clust in self.clusters:
            if sample in clust.samples:
                return clust.c_id

    def run(self, max_clusters):
        """
        runs the agglomerative clustering that in the end of the running the number of cluster
        wouldn't be bigger than max_clusters
        :param max_clusters: the maximum number of clusters that allowed in the final merging
        """
        for sample in self.samples:
            self.clusters.append(cluster.Cluster(sample.s_id, [sample]))
        while len(self.clusters) > max_clusters:
            min_dis = self.link.compute(self, self.clusters[1], self.clusters[0])
            min_clust1 = 0
            min_clust2 = 1
            for index1, clust in enumerate(self.clusters):
                for index2, other_clust in enumerate(self.clusters):
                    if clust != other_clust:
                        if min_dis > self.link.compute(self, clust, other_clust):
                            min_dis = self.link.compute(self, clust, other_clust)
                            min_clust1 = index1
                            min_clust2 = index2
            self.clusters[min_clust1].merge(self.clusters[min_clust2])
            del self.clusters[min_clust2]
        self.clusters.sort()
        sil_dict = self.compute_summery_silhouette()
        # prints the identifiers of each cluster
        for clust in self.clusters:
            clust.print_details(sil_dict[clust.c_id])
        # prints the silouette and the rand index measures of the data
        print(f"Whole data: silhouette = ", round(self.compute_summery_silhouette()[0], 3), ", RI = ",
              round(self.compute_rand_index(), 3))






