# Vector DB
- Vector databases donnot have relations.


# Graph DB
- Graph databases have relations. They are used to store data in the form of nodes and edges. Nodes represent entities and edges represent relationships between entities. 
    - Ex: Neo4j (big one)

**Note**
- Both vector db and graph db are used together, as a combination.
- Vector embeddings get the semantic meaning, graph databases get the relationships.
- It works like this: 
    - User query -> Embeddings -> Similarity Search -> Retrieve relevant chunks -> Graph DB -> Get the relations between the chunks -> Generate the answer from the query and the retrieved relevant chunks and their relations.