CALL gds.graph.create(
    "graph2", 
    "Team", 
    { played: {
            orientation: "undirected"
        }
    }
)

CALL gds.louvain.stream("graph")
YIELD nodeId, communityId
MATCH (team:Team) WHERE id(team) = nodeId
RETURN team.id AS id, communityId
ORDER BY communityId
