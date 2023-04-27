from neo4j import GraphDatabase
import time

# replace the IP address of the EC2 instance being launched
EC2_PUBLIC_IP='44.202.167.84'

URI = "neo4j://"+EC2_PUBLIC_IP+":7687"
AUTH = ("neo4j", "CS4296NEO4J")
#AUTH = ("neo4j", "reactome")

MAX_RETRIES = 3  # maximum number of retries

TIME_RECORDS=[]

QUERY_TYPE=['Node and relationship traversal','Pathfinding','Graph analytics','Text search','Data modification']

QUERIES=[
    #Node and relationship traversal 0
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
    #Pathfinding 1
    """
    MATCH (n1),(n2)
    WHERE n1.dbId = 1226097 AND n2.dbId = 9626034
    MATCH p = shortestPath((n1)-[*]-(n2))
    RETURN p
    """,
    #Graph analytics 2
    """
    CALL gds.graph.project(
    'myGraph',
    'DatabaseObject',
    'species'
    )
    YIELD graphName, nodeCount, relationshipCount
    RETURN graphName, nodeCount, relationshipCount
    """,
    #pagerank
    """
    CALL gds.pageRank.stream('myGraph')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score
    ORDER BY score DESC, name ASC
    """,
    #degree centrality
    """
    CALL gds.degree.stream('myGraph')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score AS degrees
    ORDER BY degrees DESC, name DESC
    """,
    #Text search 3
    """
    CREATE FULLTEXT INDEX dpname FOR (n:DatabaseObject) ON EACH[n.displayName]
    """,
    """
    CALL db.index.fulltext.queryNodes('dpname', 'Ontario')
    YIELD node
    RETURN node.displayName
    """,
    #Data modification 4
    """
    MATCH (n)
    WHERE ID(n) = 1
    SET n.hasDiagram = true
    RETURN n
    """,

]

def time_query(session,query):
    start_time = time.time()
    results = session.run(query)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Query took {} seconds".format(elapsed_time))
    TIME_RECORDS.append(elapsed_time)
    return results

with GraphDatabase.driver(uri=URI, auth=AUTH, connection_timeout=100) as driver:
    driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        for query in QUERIES:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    time_query(session, query)
                    break  # exit the while loop if the function call succeeds
                except Exception as e:
                    print(f"Error executing query '{query}': {e}")
                    retries += 1  # increment the number of retries
                    if retries == MAX_RETRIES:
                        print(f"Max retries ({MAX_RETRIES}) reached for query '{query}', skipping...")
                        continue

    TIME_RECORDS[2] += (TIME_RECORDS.pop(3)+TIME_RECORDS.pop(4))
    TIME_RECORDS[3] += TIME_RECORDS.pop(4)

    for (idx, i) in enumerate(TIME_RECORDS):
        time_str = "{:.3f}".format(i)
        print(QUERY_TYPE[idx]+':'+time_str)
    print('Total time:'+ str(sum(TIME_RECORDS)))
