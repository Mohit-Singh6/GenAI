# Vector DB
- Vector databases donnot have relations.
- They sure can get the chunks of semantically similar data, but they cannot get the relations between the chunks.
- So, we can't actually know what is going on between the chunks, and how they are related to each other.


# Graph DB
- Graph databases have relations. They are used to store data in the form of nodes and edges. Nodes represent entities and edges represent relationships between entities. 
    - Ex: Neo4j (big one)

**Note**
- Both vector db and graph db are used together, as a combination.
- Vector embeddings get the semantic meaning, graph databases get the relationships.
- It works like this: 
    - User query -> Embeddings -> Similarity Search -> Retrieve relevant chunks -> Graph DB -> Get the relations between the chunks -> Generate the answer from the query and the retrieved relevant chunks and their relations.


## Knowledge Graph:
- Nodes: 
    - Entities (People, Places, Things, Concepts)
    - Node has a label, properties (key-value pairs (data)), and a unique identifier.
- Edges: 
    - Relationships between entities (e.g., "is a", "part of", "related to")
- Memory like things (in chatGPT) are also stored in graph databases, as they are also relations between the entities.

## Neo4j:
- Neo4j is a graph database management system. It is not a wrapper or implementation of a graph database, but it is a full-fledged graph database management system.
- It uses Cypher QL (query language) to query the graph data. Like SQL for relational databases, Cypher is used to query graph databases.
- Neo4j can be run on cloud and self host - docker.

### Code Examples for Neo4j:
***For creating nodes:***
```
CREATE (p:Person{name: 'Mohit Singh', age: 25, gender: 'Male'})
CREATE (c:College{name: 'NIT Jalandhar', location: 'Jalandhar', established: 1987})
return p, cMATCH (p:Person{name: 'Mohit Singh'}), (c:College{name: 'NIT Jalandhar'})

CREATE (p)-[:"STUDIES AT"]->(c)
return p, c
```
***For creating relationships between nodes:***

```
MATCH (p:Person{name: 'Mohit Singh'}), (c:College{name: 'NIT Jalandhar'})

CREATE (p)-[:STUDIES_AT]->(c)
return p, c
```

***Get connections with match query:*** - get anyone who studies at a particular college
```
MATCH p=()-[:STUDIES_AT]->(:College) return p
```

***1 Edge BFS Traversal:*** - get all the connections of a particular node
```
MATCH p=(:Person{name: "Mohit Singh"})-[]->() return p
```


***Merge*** - create a node if it doesn't exist, else return the existing node


# NOTE: Chatgpt can easily generate the cypher queries for neo4j, so you can use chatgpt to create or match any nodes and relationships in neo4j. 


## Methods of storing data in graph databases:
- RAW Method:
- LangChain Method:
- Memory Method: using mem0