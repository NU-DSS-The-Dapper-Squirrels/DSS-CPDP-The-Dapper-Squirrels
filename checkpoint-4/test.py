from pyspark import *
from pyspark.sql import *
from graphframes import *
import findspark
import pandas as pd
import psycopg2

# NetworkX to visualize the graph
# import networkx as nx


findspark.init()

# # Start a Spark session
spark = SparkSession.builder.master("local[2]").getOrCreate()

# access the postgresql server
conn = psycopg2.connect(
    host="codd04.research.northwestern.edu",
    port="5433",
    database="postgres",
    user="cpdbstudent",
    password="DataSci4AI",
)

cursor = conn.cursor()

edges_query = "SELECT da1.officer_id src, da2.officer_id dst, COUNT(DISTINCT da1.allegation_id) relationship FROM data_officerallegation da1 JOIN data_officerallegation da2 ON da1.allegation_id = da2.allegation_id AND da1.officer_id < da2.officer_id GROUP BY da1.officer_id, da2.officer_id ORDER BY count(*) DESC;"
nodes_query = "SELECT  id, first_name || ' ' || last_name officer_name, allegation_count FROM data_officer;"

# Edges
cursor.execute(edges_query)
edges = cursor.fetchall()
# print("shape is: " + str(len(edges)))  # 17465
df_edges = pd.DataFrame(edges)
colnames = [desc[0] for desc in cursor.description]
df_edges.columns = colnames
print(df_edges.head(5))

# Nodes
cursor.execute(nodes_query)
nodes = cursor.fetchall()
# print("shape is: " + str(len(nodes)))  # 17465
df_nodes = pd.DataFrame(nodes)
colnames = [desc[0] for desc in cursor.description]
df_nodes.columns = colnames
print(df_nodes.head(5))


edges = spark.createDataFrame(df_edges)
nodes = spark.createDataFrame(df_nodes)
cpdb = GraphFrame(nodes, edges)
# cpdb.vertices.show()
# cpdb.edges.show()
print(cpdb.vertices.sort(["id"], ascending=True).head(5))

tc_cpdb = cpdb.triangleCount()
tc_cpdb.select("id", "count").show()

# # page rank
# pr_cpdb = cpdb.pageRank(resetProbability=0.15, tol=0.01)
# # look at the pagerank score for every vertex
# pr_cpdb.vertices.orderBy("pagerank", ascending=False).show()


def plot_graph(graph_frame):
    g = nx.DiGraph(directed=True)

    g = nx.from_pandas_edgelist(
        df_edges,
        source="src",
        target="dst",
        edge_attr="count",
        create_using=nx.DiGraph(),
    )
    g.add_nodes_from(graph_frame.vertices.toPandas()["id"])

    nx.draw(
        g,
        pos,
        with_labels=True,
        arrows=True,
        node_color=color_map,
        node_size=1000,
        font_size=10,
    )
