import sys
from data import *
from agglomerative_clustering import *
from link import *


def main(argv):
    """
    this function is the main function that runs the program
    :param argv: list of given arguments
    """
    path = argv[1]
    data = Data(path)
    samples = data.create_samples()
    print("single link:")
    agglo_single = AgglomerativeClustering(SingleLink, samples)
    agglo_single.run(7)
    print()
    print("complete link:")
    agglo_complete = AgglomerativeClustering(CompleteLink, samples)
    agglo_complete.run(7)


if __name__ == '__main__':
    main(sys.argv)
