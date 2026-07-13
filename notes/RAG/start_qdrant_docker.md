## Make a docker-compose.yml file (in any folder you like) but keep it in the same project directory




# Always run the command on the mobile hotspot, not on wifi otherwise it won't work. (I don't know why, but it works on mobile hotspot)


```yaml
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - 6333:6333
```

- Now in terminal write: 
    ```
      docker compose -f docker-compose.yml up -d
    ```

## For qdrant, we use langchain

```
pip install langchain-qdrant
```

## Now in the code: (directly from docs: https://qdrant.tech/documentation/frameworks/langchain/)

```
from langchain_qdrant import QdrantVectorStore
```