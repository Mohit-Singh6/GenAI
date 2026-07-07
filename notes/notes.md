## Vocab size:
- how many unique tokens you have is called vocab size
    - Ex: In english, you have 26 letters, so your vocab size is 52 (lower + upper case)

## A model has two phases: 
1. **Training phase**: The model is trained on a large dataset to learn the patterns and relationships between words. This phase involves adjusting the model's parameters to minimize the difference between its predictions and the actual outcomes.
Every time a output comes, we calculate the difference from the expected output and adjust the weights of the model accordingly. This is done using a process called backpropagation.

2. **Inference phase**: Once the model is trained, it can be used to generate predictions on new, unseen data. During inference, the model takes in a sequence of tokens and predicts the next token in the sequence based on the patterns it learned during training.   
**Linear Function**: Gives the probability of each token being the next token in the sequence. The token with the highest probability is selected as the model's prediction.  
**Softmax**: By changing softmax/temperature, you can control the randomness of the predictions. A higher temperature makes the output more creative and diverse, while a lower temperature makes it more focused and deterministic.

## NLP: Natural Language Processing
- Natural Language Processing (NLP) is a branch of Artificial Intelligence (AI) that helps computers understand, interpret, and generate human language.

## Synthetic Data:
- Synthetic data is artificially generated information that mimics real-world data. Rather than being collected from actual events or measurements, it is created using algorithms, mathematical models, or AI
- If models are trained on synthetic data, then the model would give very bad output/results. So it should be trained on real world data. 

## Garbage In Garbage Out (GIGO):
- If you feed a model with bad data, it will give you bad output. So the quality of the input data is very important for the model's performance.

## Prompt:
- Are Initial Tokens (Input tokens)
- If you use initial tokens/prompt created by AI, then the output will be bad.

    - **Alpaca Prompt**
        - Instructions: You are a helpful assistant that translates corporate jargon into plain English.
        - Input: "We need to leverage our core competencies to optimize our synergies and maximize our ROI."
        - Response:

    - **INST Format (LLaMA 2)**
        - [s] [/s] :
        - [INST] [/INST] : 

    - **ChatML (OpenAI)**
        {"role": "system", "content": "You are a helpful assistant."} - system prompt
        {"role": "user", "content": "Translate this corporate jargon into plain English."}

-  **Zero shot prompting**: Directly asking the model to answer a question without any additional context or examples. (In this one no system prompt is provided, so the model will answer in its default style.)

- **System Prompt**: A prompt that provides the model with instructions or context about its role or the desired behavior for generating responses.

- **Few shot prompting**: Providing the model with a few examples of the desired output format or style before asking it to generate a response. (geminiAPICalling.py)

- **Chain of Thought (CoT)**: A problem-solving approach where the model is encouraged to think through a problem step-by-step, revealing its reasoning process before providing the final answer. (calling_2.py)

- **Self consistency prompting**: A technique where the model is asked to generate multiple responses to the same question and then select the most consistent one.

- **Persona based prompting**: A technique where the model is given a specific persona or character to emulate when generating responses. Ex: 
    - "You are a wise old philosopher who speaks in riddles."
    - "You are a friendly customer support agent who always provides helpful and empathetic responses."

- **Role playing prompting**: A technique where the model is asked to assume a specific role or identity when generating responses. Ex: 
    - "You are a detective solving a mysterious case."
    - "You are a chef teaching a cooking class."
        - Difference between persona based prompting and role playing prompting is that in persona based prompting, the model is given a specific persona or character to emulate, while in role playing prompting, the model is asked to assume a specific role or identity. In persona based prompting, the model's responses are influenced by the characteristics and traits of the persona, while in role playing prompting, the model's responses are influenced by the actions and decisions of the role it is playing.

### Advanced prompting techniques: (needs orchestration) [includes good coding]

- **Contextual prompting**: A technique where the model is provided with relevant context to improve the quality of its responses.

- **Multimodal prompting**: A technique where the model is provided with multiple types of input (e.g., text, images, audio) to improve the quality of its responses.



## Difference between LLM and agent:
### 1. Large Language Model (LLM) — The Brain

* **What it is:** A core AI model trained on text.
* **Capabilities:** It processes, predicts, and generates text or code based on your prompt.
* **Limitation:** It is passive. It cannot take real-world actions or make independent decisions; it simply responds to what you type.

---

### 2. AI Agent — The Body & Actions

* **What it is:** A system that uses an LLM as its central brain, wrapped in a loop of tools and logic.
* **Capabilities:** It can actively **perceive** its environment, **plan** multiple steps, use external tools (like searching the web or executing Python code), and take autonomous actions to solve a goal.
* **Advantage:** It is active. It can loop, correct its own mistakes, and work independently.

---

#### Summary:

| Feature | LLM | AI Agent |
| --- | --- | --- |
| **Role** | The Brain / Engine | The Entire Robot (Brain + Hands) |
| **Action** | Just generates text | Executes actions (runs scripts, calls APIs) |
| **Autonomy** | Passive (Answers prompts) | Active (Runs in a loop until a goal is met) |


### 1. Running an LLM Locally

* **What it means:** Downloading an AI model directly onto your own computer or server hardware and running it without an internet connection.
* **Why do it:** You get **100% data privacy** (your data never leaves your machine), it is **completely free** to use after you buy the hardware (no API token costs), and it can work fully offline.

---

### 2. Fine-Tuning an LLM

* **What it means:** Taking an already trained, base AI model (like Llama or Mistral) and training it further on a specific, targeted dataset to alter its behavior.
* **Why do it:** It adapts the model's core brain to master a **specific tone/style** (e.g., writing like *you*), follow a strict specialized output format, or master deep, niche industry terminology that it didn’t learn well during its initial training.

---

### You can:
- Only do the inferencing of OpenAI LLM's
- While you can also train/fine-tune open source LLM's (inference also possible - obviously). 


## Ollama:

**Ollama** is a lightweight tool used to download, install, and run Large Language Models (like Llama 3.3, Mistral, or Phi) **locally on your own computer**.

It serves as the bridge that manages all the complex background setups so you don't have to deal with manual configurations.

### Key Uses:

* **One-Command Installation:** You can download and start chatting with an AI model via a single command (e.g., `ollama run llama3.3`).
* **Local API Server:** It runs a background server on your machine that exposes an OpenAI-compatible API endpoint. This allows you to connect your local models straight to Python scripts, agents, or apps like VS Code without needing an internet connection.
* **Hardware Optimization:** It automatically detects your machine's hardware (like an Nvidia GPU, Apple Silicon M-series chip, or CPU) and maximizes its speed out of the box.

In short, it makes running a private, free AI on your own hardware as simple as running an app.


## Tooling:



## Fine Tuning:
- Base Model: A pre-trained LLM that has been trained on a large, general dataset. It has a broad understanding of language and can perform a wide range of tasks, but may not be specialized in any particular domain.
- Transformers just predict the next words, the chatgpt and other chatbots are built on top of transformers, they are fine tuned to perform specific tasks like answering questions, generating code, etc.

- Full parameter fine-tuning: Updating all the parameters of the base model during training. This allows the model to learn new patterns and adapt to the specific task, but it requires a large amount of data and computational resources.
    - ***Problems:***
        - High computational cost
        - High hardware or GPU requirements
        - Self Hosting needs to be done, because the model is too big to be hosted on cloud platforms like OpenAI or Hugging Face.

    - Now for full seeing full parameter fine-tuning, you need GPU so go to google colab to check the code.
        - **In google colab: Chat Template**
            - Chat template => [{"role": "user", "content": "___"}]
                - this is how you write generally, and the tokenizer will automatically convert this to the way the model understands it. So you don't have to worry about the tokenization process, the model will automatically understand it.
            - Step 2: Prepare the dataset in the same format as the chat template, and then use the dataset to fine-tune the model.
            - Step 3: full_conversation = input_detoken + output_label + tokenizer.eos_token 
            - Step 4: Get the output, calculate the loss, and then backpropagate the loss to update the model's parameters. Do it like 10 times or so to get the model to learn the new patterns and adapt to the specific task.

            - ***Cons: ***
                - Accuracy is less

    - OpenAI or Gemini like models don't let you fine tune their models, but they do let you give the data set file in .jsonl format, and they will do the fine tuning for you. Then you can use the fine tuned model for your specific task. But open source models like LLaMA, Mistral, etc. let you do full parameter fine tuning on your own hardware.

    - There are websites like replicate, huggingface, etc. that let you do full parameter fine tuning on their cloud servers, but they charge you for it. So if you have the hardware and the data set, it is better to do it on your own hardware.

- LoRA (Low-Rank Adaptation): A parameter-efficient fine-tuning method that updates only a small subset of the model's parameters. This allows for faster training and lower resource requirements, while still achieving good performance on the specific task.
    - We will never change/update the base model's parameters
    - Till the point of calculating the loss, the steps are the same, after that instead of back propagration (which uses GPU), we will store/track the differences in a new storage (delta), 2 + 2 = 100. Diff = 96, => 2 + 2 = 100 - 96 => 4.
    - Takes up extra space but no need of GPU


- Is giving system prompt fine tuning? No, it is not fine tuning, it is just giving the model a context or instruction to follow while generating the output. Fine tuning is done by training the model on a specific dataset to adapt its parameters to perform a specific task or follow a specific style. But on application level it is kind of fine tuning, because you are giving the model a specific instruction to follow while generating the output. 


## RAG:
- RAG (Retrieval-Augmented Generation) is a technique that combines the strengths of retrieval-based methods and generative models to improve the quality and relevance of generated responses. It allows the model to access external knowledge sources (like documents, databases, or APIs) during the generation process, enabling it to provide more accurate and contextually appropriate answers.

### Difference between RAG and Fine Tuning:
- RAG: The model retrieves relevant information from external sources during inference, allowing it to generate responses based on up-to-date knowledge without modifying its internal parameters. It is useful when the knowledge base is frequently changing.

- Fine Tuning: The model's internal parameters are updated during training to adapt it to a specific task or domain. It is useful when the model needs to learn new patterns or behaviors that are not present in its original training data.

### When to use RAG and when to use Fine Tuning:
- Use RAG when you want to provide the model with access to external knowledge sources during inference, allowing it to generate responses based on up-to-date information without modifying its internal parameters. It is useful when the knowledge base is frequently changing or when user can ask kind of anything.

- Use Fine Tuning when you want to adapt the model to a specific task or domain by updating its internal parameters during training. It is useful when the model needs to learn new patterns or behaviors that are not present in its original training data. You just feed it the data set and it will learn the new patterns and adapt to the specific task. You can't do fine tuning frequently as it is costly and time consuming.

## Gemini, Claude - all these have OpenAI compatible API's, so you can use them in the same way as you use OpenAI API's. You just have to change the API endpoint (or base URL) and the API key. The rest of the code will remain the same.
- Using openAI's sdk you can call the API's of other models like Gemini, Claude, etc. without changing the code. 

## What is SDK in simple terms:
- SDK (Software Development Kit) is a set of tools, libraries, and documentation provided by a company (like OpenAI) to help developers build applications that use their services.

## RAG:
- ***Context Window***
    - The context window is the maximum number of tokens (words or pieces of words) that a language model can consider at once when generating a response. It defines how much of the conversation history or input text the model can "see" and use to generate its output.
        - Due to this limitation, we need to optimize the RAG process to ensure that the most relevant information is included in the context window for generating accurate and coherent responses because the data can be very large.
            
    - Retrieving the most relevant information from a large dataset and including it in the context window to get the best result for the query is called RAG (Retrieval-Augmented Generation). 

    - Regex: Regex, short for Regular Expression, is a sequence of characters that forms a search pattern used to find, manipulate, or validate text strings.
        Ex: %Mohit% - will match any string that contains "Mohit" in it. 

    - ***Use Case or Example of RAG***:
        - Suppose you have a pdf document and you have to answer a query related to that document:
            - Case 1: PDF is small like 1-2 pages, then you can directly feed the whole document to the model and it will give you the answer. Because the whole document will fit in the context window of the model.

            - Case 2: PDF is large like 1000 pages, then you can't feed the whole document to the model because it will exceed the context window of the model. So you have to use RAG to retrieve the most relevant information from the document and feed it to the model to get the answer.
                - To feed the most relevant info, we perform something called **INDEXING**. Indexing is a process and it can be of different types, here we will do it by dividing the document into smaller chunks and storing them in a vector database. 
                - STEPS: 
                    1. Chunking: Break the large document into smaller chunks of text
                    2. Embedding: Convert each chunk into a vector using an embedding model
                    3. Store these vectors in a vector database

                - Now user makes a query:
                    1. Query Embedding: Convert the user's query into a vector embeddings using the same embedding model
                    2. Similarity Search: Search the vector database for the most similar vectors to the query vector
                    3. From the previous step, we get the most relevant chunks of text from the document. Now we feed these chunks to the model to get the answer to the user's query.

    - ***Why do we need LangChain?***
        -  def load_pdf  
           def split_pdf  
           def convert_chunk_to_embedding  
           def save_to_pinecone  
           def search_pincode  
           def get_cunk  
           def chat  

            - All these functions are required to perform RAG, but if you have to write all these functions from scratch, it will take a lot of time and effort. And some of these functions have to be written separately for different formats like pdf, docx, txt, etc. So we need a framework that can handle all these functions and provide a unified interface to perform RAG. 