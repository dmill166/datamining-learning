# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 30: Books Recommendation System

from neo4j import GraphDatabase
import json, sys
import pandas as pd

# defintions/parameters
CONNECTION_URI   = 'bolt://localhost:7687' 
DB_USER           = 'neo4j'
DB_PASSWD         = '12345678' 

def books_read_by(conn, user_name):
    session = conn.session()
    cmd = '''
        MATCH (user: User {name: $user_name})-[r:read]->(book: Book) 
        MATCH (book)-[:is]->(g: Genre)
        RETURN r.rating AS rating, book.title AS book_title, COLLECT(g.name) AS genres
    '''
    results = session.run(
        cmd, 
        user_name=user_name
    )
    books_read = []
    for result in results.data():
        books_read.append([result['book_title'], result['rating'], result['genres']])
    books_read.sort(key=lambda x:x[1])
    return books_read

def jaccard(set_a, set_b):
    intersection = len(list(set(set_a).intersection(set_b)))
    union = (len(set_a) + len(set_b)) - intersection
    return round(intersection / union, 5)

if __name__ == "__main__":

    # command-line validation 
    if len(sys.argv) == 1:
        print(f"Use: {sys.argv[0]} genres")
        sys.exit(1)
    target_genres = sys.argv[1].split(",")
    set_a = set(target_genres)

    # connect to Neo4J 
    conn = GraphDatabase.driver(CONNECTION_URI, auth=(DB_USER, DB_PASSWD))

    # TODOd: create the "target" user profile
    session = conn.session()
    cmd = '''
        MERGE (a: User {name: 'target'})
    '''
    session.run(cmd)
    for genre in set_a:
        cmd = '''
            MATCH (a: User) WHERE a.name = 'target' 
            MATCH (g: Genre) WHERE g.name = $genre 
            MERGE (a)-[:likes]->(g)
        '''
        session.run(
            cmd, 
            genre=genre
        )
        
    # TODO: query for all user nodes (indirectly) connected to the given user by genre
    session = conn.session()
    cmd = '''
        MATCH (a: User)-[:likes]->(:Genre)<-[:likes]-(b:User) 
        WHERE a.name = 'target' 
        WITH b
        MATCH (b)-[:likes]->(g:Genre)
        WITH b.name AS user_name, COLLECT(g.name) AS genres 
        RETURN user_name, genres
    '''
    results = session.run(
        cmd    
    )
    # print(results.data()[0])

    # TODO: create a dataframe with most similar users and their book recommendations
    df = pd.DataFrame(columns=['user_name', 'jaccard', 'recommended'])
    for result in results.data():
        user_b_name = result['user_name']
        set_b = set(result['genres'])
        books_recomm = []
        for book_title, rating, genres in books_read_by(conn, user_b_name):
            genre_match = False 
            for genre in genres:
                if genre in set_a:
                    genre_match = True 
                    break 
            if genre_match:
                books_recomm.append(book_title)
        if len(books_recomm) > 0 and rating >= 4:
            df = df.append(
                {
                'user_name': user_b_name, 
                'jaccard': jaccard(set_a, set_b),
                'recommended': books_recomm
                }, 
                ignore_index = True
            )
    #print(df)

    # TODO: display top 10 dataframe rows sorted by jaccard in descending order
    df.sort_values(by=['jaccard'], ascending=(False), inplace=True)
    print(df)

    # TODO: delete "target" user profile
    # session = conn.session()
    # cmd = '''
        
    # '''
    # session.run(cmd)