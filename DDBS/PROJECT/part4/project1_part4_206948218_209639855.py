# -*- coding: utf-8 -*-
"""project1_part1_206948218_209639855.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-XdPwHc9DYtfUYbfVs9RSnbi7q2HIcRe

#Part 1 - Extract and Transform
---
"""


# importing
import os
import re
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import substring
from pyspark.sql.functions import from_json
from pyspark.sql.functions import col,lit
from pyspark.sql.functions import when
from pyspark.sql.functions import size
from pyspark.sql.functions import array_remove ,array_contains , array_intersect
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from IPython.display import display_html 
from pyspark.sql.types import StructField, StructType, StringType, DoubleType, IntegerType , DataType ,LongType , ArrayType , json , DateType

def init_spark(app_name: str):
  spark = SparkSession.builder.appName(app_name).getOrCreate()
  sc = spark.sparkContext
  return spark, sc

spark, sc = init_spark('demo')
sc

#files
file_credits='credits.csv'
file_movies='movies.csv'
file_queries='queries.csv'
file_tickets='tickets.csv'
file_users='users.csv'

#loading the users file
users = spark.read.option("Header", "true")\
        .option("multiline", "true")\
        .option("escape", "\"")\
        .csv(file_users)

#loading the movies file
movies = spark.read.option("Header", "true")\
        .option("multiline", "true")\
        .option("escape", "\"")\
        .csv(file_movies)
#transformations for movies
## dropping irrelevant columns
cols_to_drop_movies = ['overview', 'revenue', 'tagline']
movies = movies.drop(*cols_to_drop_movies)

##extracting from relase_date column the year
movies = movies.withColumn('release_date', substring('release_date', 7,9))

##extracting necessary information from the structured columns
columns = ['genres', 'production_companies', 'production_countries', 'spoken_languages', 'cities']
schema = ['array<struct<id:int , name:string>>',
              'array<struct<name:string, id:int>>', 
              'array<struct<iso_3166_1:string , name:string>>',
              'array<struct<iso_639_1:string , name:string>>',
              'array<string>']

for column, field in zip(columns, schema):
    movies = movies.withColumn(column, from_json(col(column), lit(field)))

movies = movies.withColumn('genres', movies.genres['name']).withColumn('production_companies', movies.production_companies['name'])\
    .withColumn('production_countries', movies.production_countries['name']).withColumn('spoken_languages', movies.spoken_languages['name'])\
    .withColumn('spoken_languages', array_remove('spoken_languages', "?????")).withColumn('spoken_languages', array_remove('spoken_languages', "??????"))\
    .withColumn('spoken_languages', array_remove('spoken_languages',""))

#loading the credits file using pandas and regex
credits_pd = pd.read_csv('credits.csv')
credits_pd['cast']= [ re.findall("(?<='name':\s)'[\w]*[(\._\-\s)*\w*]*'", i, flags=0) for i in credits_pd['cast'] ]
credits_pd['crew']= [ re.findall("(?<='Director', 'name':\s)'[\w]*[(\._\-\s)*\w*]*'", i, flags=0) for i in credits_pd['crew'] ]
credits =  spark.createDataFrame(credits_pd)

#loading the queries file
queries = spark.read.option("Header", "true")\
        .option("multiline", "true")\
        .option("escape", "\"")\
        .csv(file_queries)

##extracting from relase_date column the year
queries = queries.withColumn('from_realese_date', substring('from_realese_date', 3,4))

#loading the tickets file
tickets = spark.read.option("Header", "true")\
        .option("multiline", "true")\
        .option("escape", "\"")\
        .csv(file_tickets)

cols_to_drop_tickets = ['cinema_id']
tickets = tickets.drop(*cols_to_drop_tickets)

"""#Part 3 - Deploy via Spark
---


"""

#join movies to credits
movies=movies.join( credits,movies.movie_id==credits.id,"inner")

#Jerusalem
hebrew= '×¢Ö´×Ö°×¨Ö´××ª'
Jerusalem = movies.filter(array_contains(movies.cities,'Jerusalem') )
tel_no_j = movies.filter(~array_contains(movies.cities,'Jerusalem')).filter(array_contains(movies.cities,'Tel Aviv'))
Jerusalem= Jerusalem.union(tel_no_j)
Jerusalem= Jerusalem.drop(*['crew','id']).filter(Jerusalem.release_date >=1990)
Jerusalem_1 = Jerusalem.filter(array_contains(Jerusalem.production_countries,'Israel')).filter(array_contains(movies.spoken_languages,hebrew))
a= Jerusalem.filter(array_contains(Jerusalem.production_countries,'Israel')).filter(~array_contains(movies.spoken_languages,hebrew))
Jerusalem_2 = Jerusalem.filter(~array_contains(movies.spoken_languages, hebrew)).union(a)
#Jerusalem_1.show(5)
#Jerusalem_2.show(5)

#Haifa
Haifa = movies.filter(array_contains(movies.cities, 'Haifa'))
Haifa = Haifa.drop(*['production_countries', 'id']).filter(Haifa.release_date >=2010)
Haifa_1=Haifa.filter(array_contains(Haifa.genres, 'Drama'))
Haifa_2 = Haifa.filter(~array_contains(Haifa.genres, 'Drama'))
#Haifa_1.show(5)
#Haifa_2.show(5)

#Tel Aviv
Tel_Aviv = movies.filter(array_contains(movies.cities, 'Tel Aviv'))
Tel_Aviv = Tel_Aviv.drop(*['production_countries', 'crew', 'id']).filter(Tel_Aviv.release_date >= 2010)
Tel_Aviv_1 = Tel_Aviv.filter(array_contains(Tel_Aviv.genres, 'Action'))
Tel_Aviv_2 = Tel_Aviv.filter(~array_contains(Tel_Aviv.genres, 'Action'))
#Tel_Aviv_1.show(5)
#Tel_Aviv_2.show(5)

#Eilat
Eilat = movies.filter(array_contains(movies.cities, 'Eilat'))
Eilat=Eilat.drop(*['cities','crew','cast','id']).filter(Eilat.release_date >=1990)
Eilat_1 = Eilat.filter(array_contains(Eilat.production_companies, 'Walt Disney Pictures'))
b= Eilat.filter(~array_contains(Eilat.production_companies, 'Walt Disney Pictures')).filter(array_contains(Eilat.production_companies,'Warner Bros.'))
c= Eilat.filter(~array_contains(Eilat.production_companies, 'Walt Disney Pictures')).filter(~array_contains(Eilat.production_companies,'Warner Bros.'))
Eilat_2= c.filter(~array_contains(Eilat.production_companies,'Pixar Animation Studios'))
c=c.filter(array_contains(Eilat.production_companies,'Pixar Animation Studios'))
Eilat_1=Eilat_1.union(b).union(c)
# Eilat_1.show(5)
# Eilat_2.show(5)

#Tiberias
Tiberias = movies.filter(array_contains(movies.cities, 'Tiberias'))
Tiberias = Tiberias.drop(*[ 'crew', 'id']).filter(Tiberias.release_date >= 1990)
Tiberias_1 = Tiberias.filter(array_contains(Tiberias.genres, 'Family')).filter(array_contains(Tiberias.genres, 'Documentary'))
a =Tiberias.filter(array_contains(Tiberias.genres, 'Family')).filter(~array_contains(Tiberias.genres, 'Documentary'))
Tiberias_2 = Tiberias.filter(~array_contains(Tiberias.genres, 'Family')).union(a)
# Tiberias_1.show(5)
# Tiberias_2.show(5)