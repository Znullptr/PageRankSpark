from pyspark.sql import SparkSession
from graphframes import GraphFrame
import sys

# Create a SparkSession
spark = SparkSession.builder.appName("PageRank").getOrCreate()

# Load the psxhax pages data from CSV as a DataFrame
pages_info_df = spark.read.csv(sys.argv[1], header=True)

# Create vertices DataFrame
vertices_df = pages_info_df.select("page_id").withColumnRenamed("page_id", "id")


# Function to split links
def split_links(row):
    page_id, links = row
    if links is not None:
        links = [link.strip() for link in links.split(",")]
    else:
        links = []
    return [(page_id, link) for link in links]


# Select each link and its corresponding page_id from pages_info_df
links_rows = pages_info_df.select("page_id", "links").rdd.flatMap(split_links).collect()

# Create edges_list to store all the edges of the graph
edges_list = []
for row in links_rows:
    src_page_id, link = row
    matching_row = pages_info_df.filter(pages_info_df.page_url == link).select("page_id").first()
    if matching_row is not None:
        dest_page_id = matching_row.page_id
        edges_list.append((src_page_id, dest_page_id))

# Create edges DataFrame from the list
edges_df = spark.createDataFrame(edges_list, ["src", "dst"])

# Create GraphFrame
graph = GraphFrame(vertices_df, edges_df)

# Run PageRank algorithm
page_rank = graph.pageRank(maxIter=50, resetProbability=0.15)

# Get the PageRank scores as a DataFrame
page_rank_df = page_rank.vertices.select("id", "pagerank").withColumnRenamed("id", "page_id")

# Join with the original DataFrame to add PageRank scores
pages_info_df_with_rank = pages_info_df.join(page_rank_df, on="page_id", how="inner")

# Sort the psxhax pages based on PageRank scores
ranked_pages_df = pages_info_df_with_rank.orderBy("pagerank", ascending=False)

# Save the ranked psxhax pages information to CSV
output_path = "hdfs://Master:9000/user/hadoop/outputs/spark_outputs/ranked_psxhax_pages"
ranked_pages_df.write.csv(output_path, header=True, mode="overwrite")

# Stop the SparkSession
spark.stop()
