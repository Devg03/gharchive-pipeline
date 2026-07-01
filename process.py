import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("gharchive-processing").getOrCreate()

df = spark.read.json("data/raw")

df.printSchema()
df.show(5, truncate=False)

events = df.select(
    col("type"),
    col("repo.name").alias("repo_name"),
    col("created_at"),
    col("year"),
    col("month"),
    col("day"),
    col("hour")
)

events.show(5)

event_types = ["PushEvent", "WatchEvent", "ForkEvent", "PullRequestEvent", "IssuesEvent"]
filtered = events.filter(col("type").isin(event_types))

print("before filter:", events.count())
print("after filter:", filtered.count())
