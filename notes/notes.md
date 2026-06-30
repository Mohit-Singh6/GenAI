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