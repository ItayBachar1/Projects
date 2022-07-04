def kmeans_fit(data ,k,max_iter ,q ,init):
    import numpy as np
    import findspark
    findspark.init()
    from pyspark.sql import SparkSession
    def init_spark(app_name: str):
        spark = SparkSession.builder.appName(app_name).getOrCreate()
        sc = spark.sparkContext
        return spark, sc
    spark, sc = init_spark('hw2')
    def vector_to_closest_cluster(initt ):
        def innerF(point):
            min_dist=-1
            closest =-1
            count =0
            for cent in initt:
                #dd = round(sum([(xi - yi) ** 2 for xi, yi in zip(point, cent)]),4)
                dd = sum([(xi - yi) ** 2 for xi, yi in zip(point, cent)])
                if ( min_dist== -1 or dd < min_dist):
                    closest=count
                    min_dist=dd
                count+=1
            if ( min_dist== -1 ):
                print(f" vector: { point} failed to find any closter center to next to .  cluster list:{ initt}")
            return (closest,min_dist**.5,point)
        return innerF
        # clo = cluster num , distance from clus , [vctor]


    for i in range(max_iter):

        data_rows=data.rdd.map(lambda row : [x for x in row])
        calc_closest_dist_vect=vector_to_closest_cluster(init)
        prossed_vectors=data_rows.map(lambda x: calc_closest_dist_vect(x)).groupBy( lambda row: row[0])
        def mean_after_drop_q(vec_in_clus,q):
            vec_in_clus.sort(key=lambda row: row[1])
            #vec_in_clus isnt empty thanks to groupby
            dim = len(vec_in_clus[0][2])
            sum_vector =np.array([0]*dim)
            count=0
            for vecc in vec_in_clus:
                count+=1
                if(count%q !=0):
                    sum_vector =sum_vector+np.array(vecc[2])
            count = count - np.floor(count/q)
            sum_vector = np.round(sum_vector/ count,3)
            return sum_vector.tolist()
        new_init_rdd=prossed_vectors.map(lambda x : mean_after_drop_q(list(x[1]),q))
        new_init=new_init_rdd.collect()
        no_missmatch = True
        if len(new_init)== len (init):
            for ii in range(len (init)):
                if (not no_missmatch):
                    break
                for jj in range(len(init[0])):
                    if init[ii][jj]!=new_init[ii][jj]:
                        no_missmatch=False
        else:
            no_missmatch=False
        init=new_init
        if (no_missmatch ):
            return spark.createDataFrame(init)
    return spark.createDataFrame(init)