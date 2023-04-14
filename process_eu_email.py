import csv

input_file = 'Email-EuAll.txt'

# Convert to format that neo4j will accept
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader((line for line in infile if not line.startswith('#')), delimiter='\t')
    edges = open('email-EuAll-edges.csv', 'w', newline='', encoding='utf-8')
    nodes = open('email-EuAll-nodes.csv', 'w', newline='', encoding='utf-8')

    edges_writer = csv.writer(edges)
    nodes_writer = csv.writer(nodes)

    nodes_set = set()
    for row in reader:
        from_node = row[0]
        to_node = row[1]
        if from_node not in nodes_set:
            nodes_writer.writerow([from_node])
            nodes_set.add(from_node)
        if to_node not in nodes_set:
            nodes_writer.writerow([to_node])
            nodes_set.add(to_node)
        edges_writer.writerow([from_node, to_node])
    edges.close()
    nodes.close()
