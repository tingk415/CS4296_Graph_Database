from neo4j import GraphDatabase
import time

# replace the IP address of the EC2 instance being launched
EC2_PUBLIC_IP='3.95.138.150'

URI = "neo4j://"+EC2_PUBLIC_IP+":7687"
#AUTH = ("neo4j", "CS4296NEO4J")
AUTH = ("neo4j", "reactome")

QUERIES=[
    #Node and relationship traversal
    """
    MATCH (n)
    WITH n, RAND() AS rand
    ORDER BY rand
    LIMIT 1000
    WITH COLLECT(ID(n)) AS nodeIds
    UNWIND nodeIds AS nodeId
    MATCH (m)-[r1]->()-[r2]->()
    WHERE ID(m) = nodeId
    RETURN nodeId, count(r2) AS secondhopRelationshipCount
    """,
    #Pathfinding
    """
    MATCH (n1),(n2)
    WHERE n1.dbId = 1226097 AND n2.dbId = 9626034
    MATCH p = shortestPath((n1)-[*]-(n2))
    RETURN p
    """,
    #Graph analytics
    """
    CALL algo.pageRank('Node', 'INTERACTS_WITH', {iterations: 20})
    YIELD nodeId, score
    RETURN algo.getNodeById(nodeId).displayName AS name, score
    ORDER BY score DESC
    LIMIT 10
    """,
    """
    CALL algo.betweenness('Node', 'INTERACTS_WITH', {direction: 'both'})
    YIELD nodeId, centrality
    RETURN algo.getNodeById(nodeId).displayName AS name, centrality
    ORDER BY centrality DESC
    LIMIT 10
    """,
    #Data modification
    """
    CREATE (n:Node {displayName: $name, species: $species})
    """,
    """
    MATCH (n)-[r:INTERACTS_WITH]->(m)
    WHERE id(n) = $nodeId
    DELETE r
    """,
    #Text search
    """
    CALL db.index.fulltext.queryNodes('displayName', $keyword)
    YIELD node
    RETURN node.displayName, node.species
    """

]


def time_query(session,query):
    start_time = time.time()
    results = session.run(query)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Query took {} seconds".format(elapsed_time))
    return results


with GraphDatabase.driver('bolt://localhost:7687', auth=AUTH) as driver:
    driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        for query in QUERIES:
            time_query(session,query)
