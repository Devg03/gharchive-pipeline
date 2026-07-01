import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("gharchive-processing").getOrCreate()

df = spark.read.json("data/raw")

df.printSchema()
df.show(5, truncate=False)
