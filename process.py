import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import count

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

# Filter only the columns with the specific event types
event_types = ["PushEvent", "WatchEvent", "ForkEvent", "PullRequestEvent", "IssuesEvent"]
filtered = events.filter(col("type").isin(event_types))

print("before filter:", events.count())
print("after filter:", filtered.count())

# Most active repos - event count (agg)
repo_activity = (
    filtered
    .groupBy("repo_name")
    .agg(count("*").alias("event_count"))
    .orderBy(col("event_count").desc())
)

repo_activity.show(10, truncate=False)

# Events by type (agg)
events_by_types = (
    filtered
    .groupBy("type")
    .agg(count("*").alias("events_by_type"))
    .orderBy(col("events_by_type").desc())
)

events_by_types.show()