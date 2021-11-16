# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 28: Louvain

from neo4j import GraphDatabase
import csv,os

# defintions/parameters
CONNECTION_URI       = 'bolt://localhost:7687' 
DB_USER              = 'neo4j'
DB_PASSWD            = '12345678'
DATA_FOLDER          = '../data/'
KARATE_TSV_FILE      = 'karate_club_network.txt'
COMMUNITIES_CSV_FILE = 'communities.csv'

if __name__ == "__main__":

    # connect to Neo4J 
    conn = GraphDatabase.driver(CONNECTION_URI, auth=(DB_USER, DB_PASSWD))

    # TODO (part 1): create nodes & relationships from TSV file

    # the query below should display "#nodes [{'COUNT(n)': 34}]""
    session = conn.session()
    cmd = '''
        match (n) RETURN COUNT(n)
    '''
    results = session.run(cmd)
    print('#nodes', str(results.data()))

    # TODO (part 2): import communities and set community "types"



