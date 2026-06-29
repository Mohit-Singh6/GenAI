# Chatgpt works on next word prediction

- GPT: Generative Pre-trained Transformer: It can't tell what is the weather currently but ChatGPT can, becuase ChatGPT is GPT + Agent, while GPT is just an LLM
- GPT works on pre-trained data not real world data.

## Phase 1: Input and encoding
- INPUT: The cat sat on the mat
- Step 1: Tokenization process (let's say 1 token for 1 word) => 6 tokens
- Now let's say there is a big dictionary where every token is given a number:
    - The - 1
    - Cat - 10
    - Sat - 76
    - on - 100
    - Mat - 98

- Step 2: Vector embedding of these tokens are generated using a pre-trained model (like BERT, GPT, etc.) [Instead of using a separate model like BERT, the LLM utilizes its own internal, learned embedding layer] which converts these tokens into high-dimensional vectors that capture semantic meaning.
    - Semantic meaning: The meaning of a word in context, which can be captured by its relationships with other words in a sentence or document.
        - Ex: Mars - red planet,    Earth - blue planet

- Step 3: Postional Encoding: 
    - The order of the tokens is important for understanding the meaning of a sentence. Positional encoding is added to the token embeddings to give the model information about the position of each token in the sequence.
    - Ex: "The cat sat on the mat" vs "On the mat sat the cat" have different meanings due to word order.
    - So the final input to the model is a combination of the token embeddings and their positional encodings.

- Step 4: Self Attention Mechanism: 
    - The self-attention mechanism allows the model to weigh the importance of each token in the input sequence relative to the others. This helps the model understand context and relationships between words.
    - It allows the tokens to "attend" to each other, meaning that the model can focus on relevant tokens when making predictions. So that they can adjust there embeddings based on the context of the entire sequence.
    - ### Multi-Head Attention: 
        - Instead of having a single attention mechanism, the model uses multiple attention heads to capture different types of relationships between tokens. Each head learns to focus on different aspects of the input sequence, allowing the model to capture a richer understanding of the context. Ex: One head might focus on verbs, another on subject-object relationships, and another on punctuation, stitching together a highly sophisticated structural map.

- Step 5: Feed-Forward Network (FFN) Processing:
    - After the attention heads calculate where to look, the context-rich vectors are passed through a series of dense neural network layers (the Feed-Forward Network).
    - This step applies deeper, non-linear reasoning to the contextual data. It handles the heavy-duty logic and cross-references the sentence patterns against the vast world facts and rules stored in the model's parameters.

- Step 6: Linear Layer Projection:
    - Once the final Transformer layer finishes calculating, the abstract mathematical vector representing the entire sentence sequence is sent through a final Linear layer.
    - This layer acts as a massive map projection, blowing the hidden vector back up to match the exact size of the model's vocabulary dictionary (the dictionary from Step 1). It outputs a raw score (called a logit) for every single possible word in its vocabulary.

- Step 7: Softmax and Token Selection:
    - The raw vocabulary scores are processed through a mathematical Softmax function, converting those scores into clean percentage probabilities that all add up to 100%. - Ex: The model determines there is a 91% chance the next token is ".", a 4% chance it is "happily", and a 0.1% chance it is "banana".
    - The system picks a token based on these probabilities (factoring in your temperature and top_p settings).
    - OUTPUT: "." (The complete sentence becomes: "The cat sat on the mat.")


### Does self and multi head attention both occur in this process?
- Yes, both occur because they are not separate things—Multi-Head Attention is simply running Self-Attention multiple times in parallel.


# Starting with coding:
- python -m venv venv
    - **python -m venv venv creates a Virtual Environment (a isolated folder usually named venv).  
    - Instead of installing packages globally (which can break other projects if versions clash), all libraries you install via pip stay locked inside this specific folder.**
- .\venv\Scripts\Activate.ps1
    - You must activate it to tell your terminal: "Hey, temporarily ignore my global Python setup and use the isolated Python and pip inside this venv folder." If you don't activate it, running pip install will still install packages globally, defeating the whole purpose.
- pip install tiktoken (for tokenization)
- pip freeze > requirements.txt
    - This is exactly like running a script that generates your package.json dependencies list, lock-file style.
- pip install dotenv (for environment variables)
- In file: 
    - from dotenv import load_dotenv
    - load_dotenv()  # Load environment variables from .env file
- pip install groq (becasue gemini fuk gaya)
- Copy same things from docs (https://console.groq.com/docs/quickstart)