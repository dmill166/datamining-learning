# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Student: 
# Description: Homework 09 (Louvain Clustering)

from neo4j import GraphDatabase
import csv,os

# defintions/parameters
# 
CONNECTION_URI       = 'bolt://localhost:7687'
DB_USER              = 'neo4j'
DB_PASSWD            = '12345678'
DATA_FOLDER          = '../data/'
GAMES_TSV_FILE      = 'games.tsv'

if __name__ == "__main__":

    # connect to Neo4J 
    conn = GraphDatabase.driver(CONNECTION_URI, auth=(DB_USER, DB_PASSWD))

    # TODO (part 1): create nodes & relationships from TSV file
    # hint: label the nodes as "Team" and the relationships as "played"

    # the query below should display "#nodes [{'COUNT(n)': 115}]""
    session = conn.session()
    cmd = '''
        match (n:Team) RETURN COUNT(n)
    '''
    results = session.run(cmd)
    print('#nodes', str(results.data()))

    # TODO (part 2): import communities and set community "types"
    # hint: run graph.cypher statements on Neo4J desktop and export the output to communities.csv
    