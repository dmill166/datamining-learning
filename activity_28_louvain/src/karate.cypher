CALL gds.graph.create(
    "graph", 
    "Person", 
    { knows: {
            orientation: "undirected"
        }
    }
)

CALL gds.louvain.stream("graph")
YIELD nodeId, community
MATCH (person:Person) WHERE id(person) = nodeId
RETURN person.id AS id, community
ORDER BY community
