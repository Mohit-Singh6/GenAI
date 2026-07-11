# Routing

## Logical Routing
 - It points to the correct data in the dataset based on the user query. So that on similarity search, we get the correct relevant chunks from the database not randomly.
    - Ex: system_prompt: "I have 3 databases:
        1. Database 1: Python Programming
        2. Database 2: Java Programming
        3. Database 3: C++ Programming"
        
        Which is the best database for the user query: "How to convert sets to lists in python?"
    
    - Similarly we can have multiple LLM models, and we can route the user query to the correct LLM model that is best for the that user query. 


## Semantic Routing
- Let's say that, my web pages have only 4-5 options, nothing else, and those options work only at certain prompts that only I know about. So whenever a user will give a prompt, I'll ask the LLM to convert the user's prompt into a version of my prompt, so that it can work.