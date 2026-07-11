import warnings
warnings.filterwarnings("ignore") # Suppresses warnings from langchain_docling - they are not relevant to the RAG example. It still doesn't fucking work. Warnings still show up.

from dotenv import load_dotenv
load_dotenv() # Injects HF_TOKEN directly into system variables where httpx reads it

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


web_data_map = {
    # "chai-aur-html": [
    #     "https://docs.chaicode.com/youtube/chai-aur-html/welcome/",
    #     "https://docs.chaicode.com/youtube/chai-aur-html/html-intro/",
    #     "https://docs.chaicode.com/youtube/chai-aur-html/emmet-crash-course/",
    #     "https://docs.chaicode.com/youtube/chai-aur-html/common-html-tags/"
    # ],
    # "chai-aur-git": [
    #     "https://docs.chaicode.com/youtube/chai-aur-git/welcome/",
    #     "https://docs.chaicode.com/youtube/chai-aur-git/introduction/",
    #     "https://docs.chaicode.com/youtube/chai-aur-git/terminology/",
    #     "https://docs.chaicode.com/youtube/chai-aur-git/behind-the-scenes/",
    # ],
    "chai-aur-cpp": [
        "https://docs.chaicode.com/youtube/chai-aur-c/welcome/",
        "https://docs.chaicode.com/youtube/chai-aur-c/introduction/",
        "https://docs.chaicode.com/youtube/chai-aur-c/hello-world/",
        "https://docs.chaicode.com/youtube/chai-aur-c/variables-and-constants/",
        "https://docs.chaicode.com/youtube/chai-aur-c/data-types/",
    ],
    # "chai-aur-django": [
    #     "https://docs.chaicode.com/youtube/chai-aur-django/welcome/",
    #     "https://docs.chaicode.com/youtube/chai-aur-django/introduction/",
    #     "https://docs.chaicode.com/youtube/chai-aur-django/jinja-templates/",
    # ],
    # "chai-aur-sql": [
    #     "https://docs.chaicode.com/youtube/chai-aur-sql/welcome/",
    #     "https://docs.chaicode.com/youtube/chai-aur-sql/introduction/",
    #     "https://docs.chaicode.com/youtube/chai-aur-sql/postgres/",
    #     "https://docs.chaicode.com/youtube/chai-aur-sql/normalization/",
    # ],
    # "chai-aur-devops": [
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/welcome/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/setup-vpc/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/setup-nginx/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/nginx-rate-limiting/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/nginx-ssl-setup/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/node-nginx-vps/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/postgresql-docker/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/postgresql-vps/",
    #     "https://docs.chaicode.com/youtube/chai-aur-devops/node-logger/"
    # ]
}


for coll, pages in web_data_map.items():
    for page in pages:

        print(f"{coll}: {page}")

        loader = WebBaseLoader(
            web_paths=(page,)
        )

        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,      # Absolute max character limit per chunk
            chunk_overlap=200     # Keeps context overlapping at the cuts
        )

        # This recursively processes the sections and chops down anything that is too big
        final_chunks = text_splitter.split_documents(docs)


            # Embedding:

        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        # We set output_dimensionality to 768 for balanced performance and memory consumption (you can leave out that parameter to use the default dimensionality)
        embedder = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2",
            output_dimensionality=768
        )


            # Storing in Qdrant (vector db):

        from langchain_qdrant import QdrantVectorStore


            # First time creating the collections then you have to run this code to create the collection in Qdrant. After that, you can comment it out and just use the `QdrantVectorStore.from_existing_collection()` line to add more documents to the existing collection. Otherwise it would throw an error that the collection doesn't exist.

        doc_store = QdrantVectorStore.from_documents( 
            documents=[],
            embedding=embedder, # The embeddings object is used to convert text into vectors for storage and retrieval in the vector database.
            collection_name=coll, # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
            url="http://localhost:6333/",
            # Send only 60 text vectors per batch to stay safely under Google's 100 limit
            batch_size=60
        )

        # After the first time, you can use the following code to add more documents to the existing collection without creating a new one.
        # doc_store = QdrantVectorStore.from_existing_collection(
        #     embedding=embedder,
        #     collection_name=coll, # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
        #     url="http://localhost:6333/"
        # )


            # For ingestion of the pdf's vector embeddings in the database
        doc_store.add_documents(
            documents=final_chunks,
            batch_size=60  # 💻 Tells the embedding engine to step down and wait
        ) # Adds the final chunks of text to the Qdrant collection for later retrieval based on vector similarity.
        # print("Ingestion done!")

    print("\n")