## Query Translation
- If  user queries are ambiguous then the output will also be ambiguous or bad or not accurate [Garbage in Garbage Out]
- So, you can never trust the user query. 
- If you can convert "What user asked" to "What user actually wants to know", then it would make the the RAG system better/more accurate.

### Abstraction
- If user query is ambiguous then we can use a LLM to convert the user query to a more specific query.

***We have to maintain the balance between abstraction and less abstraction/specificity. If we make the query too specific then we might lose some relevant information.***


### Parallel Query (Fan Out) Retrieval
- From the user query, we can generate multiple queries from AI and then we can apply similarity search for each of the queries and then we do the union of all the results/chunks (remove duplicates)
- After that we get the original user query and the retrieved chunks and then we can generate the answer from that using LLM.

**Fan Out Architecture**: Fan out architecture is a design pattern where a single request or query is distributed across multiple processing units or services, allowing for parallel processing and improved performance. In the end combining the results from these parallel processes to produce a final output. 

## Approach 1:
- Re-write user query using AI
    - **Reciprocate Rank Fusion (RRF)**: In this approach, instead of doing union of all the results/chunks, we can rank the results based on how many times they appear and on which rank they appear, then we can take the top N results/chunks and then we can generate the answer from that using LLM.

    - **Query Decomposition**: Till now we weren't doing any abstraction or less abstraction things:
        - ***Abstraction***:
                |
                To
                |
                V
        - ***Less Abstraction***: 
            - **CoT (Chain of Thought)**: In this approach, we can ask the AI to generate the answer in a step by step manner. This will help the AI to think more and generate a better answer. [Breaking down the problem into smaller sub-problems]

        - During the chain of thought, we can ask the AI to generate multiple queries and then we can apply similarity search for each of the queries and every time or step, we generate the output with the current query and the retrieved chunks for that step's similarity search. And that output (along with it's query) is then added to the context, and we keep on repeating till the main query is not answered.
        - Then we take all the generated outputs from each query, and generate a combined output from all of outputs and the main (original) query. That is the final response.
        - Unlike RRF, in this one we don't and we can't answer all the generated queries at once, we have to answer them one by one and then combine the outputs. So, this approach is more time consuming but it will give better results than RRF.

        ## Time increases, Accuracy increases and also vice versa.

        - The accuracy of query decomposition is better than RRF but it consumes more time. 
        - You have to choose accordingly based on your use case. 

    - **Making the prompt more abstract (Step Back Prompting)**: [Take a step back - white paper by Google]
        - In this approach, we can ask the AI to generate a more abstract query from the user query. This will help the AI to think more and generate a better answer. [Making the prompt more abstract]
        - For example, if the user query is "WHen is lionel messi's birthday?", then we can ask the AI to generate a more abstract query like "What are lionel messi's personal details?".
        - Then we can apply similarity search for this abstract query and then we can generate the answer from that using LLM.


    - ***HyDE (Hypothetical Document Embedding)***: [**Less abstraction**]
        - *Problem*: It needs large models to work, doesn't works well with smaller models.
        - *Problem*: Doesn't works with legal documents, because it generates hypothetical documents which might not be legally correct.
        - Method:
            - We can ask the AI to generate a hypothetical document from the user query. This will help the AI to think more and generate a better answer. [**Less abstraction**]
            - For example, if the user query is "WHen is lionel messi's birthday?", then we can ask the AI to generate a hypothetical document like "Lionel Messi is an Argentine professional footballer who plays as a forward for Inter Miami and the Argentina national team. Lionel Messi was born on June 24, 1987 in Rosario, Argentina. He is widely regarded as one of the greatest footballers of all time."
            - Then we apply the similarity search for this hypothetical document (by generating it's vector embedding) and then we can generate the answer from that & the original query using LLM.

