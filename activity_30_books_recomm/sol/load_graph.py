# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 30: Books Recommendation System

from neo4j import GraphDatabase
import json

# defintions/parameters
CONNECTION_URI   = 'bolt://localhost:7687' 
DB_USER           = 'neo4j'
DB_PASSWD         = '12345678' 

# connect to Neo4J 
conn = GraphDatabase.driver(CONNECTION_URI, auth=(DB_USER, DB_PASSWD))

# read all books
with open('../data/books.json', 'rt') as books_file, open('../data/users.json', 'rt') as users_file:
    books = json.load(books_file)
    users = json.load(users_file)
        
    # create "book" and "genre" nodes 
    session = conn.session()
    for book in books:
        for genre in book['genres']:
            cmd = '''
                MERGE (book: Book {title: $title, author: $author})
                MERGE (genre: Genre {name: $genre})
                CREATE (book)-[r: is]->(genre)
            '''
            session.run(
                cmd, 
                title=book['title'],
                author=book['author'],
                genre=genre
            )
    
    # create "user" nodes 
    session = conn.session()
    for user in users:
        for book, rating in user['books_read']:
            cmd = '''
                MATCH (book: Book) WHERE book.title = $title
                MERGE (user: User {name: $name})
                MERGE (user)-[:read {rating: $rating}]->(book)
            '''
            session.run(
                cmd, 
                name=user['name'],
                title=book['title'],
                rating=rating
            )
            for genre in book['genres']:
                cmd = '''
                    MATCH (genre: Genre) WHERE genre.name = $genre
                    MERGE (user: User {name: $name})
                    MERGE (user)-[:likes]->(genre)
                '''
                session.run(
                    cmd, 
                    genre=genre,
                    name=user['name']
                )

# close the connection
conn.close()
