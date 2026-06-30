Because **the official Ollama SDK libraries handle all of that networking heavy lifting for you under the hood.**

When you used `ollama.chat()` in Python or JS, you didn't see any URLs, route handlers, or JSON payloads, but your code was secretly performing the exact same actions you would manually test inside Thunder Client or Postman.

Here is exactly why you didn't need to configure those layers manually:

### 1. Ollama is already running its own server

When you downloaded and launched the Ollama desktop app, it started a persistent background engine on your machine. This engine acts as a pre-configured web server listening continuously on port `11434`.

You didn't need to write a route handler (like an Express.js `app.post('/api')` block) because **Google/Ollama engineers already wrote it for you inside the application binary.** The server is already sitting there, completely idle, waiting for incoming network connections.

### 2. The SDK acts as your built-in Thunder Client

Instead of opening Thunder Client, manually setting the dropdown to `POST`, typing out `http://localhost:11434/api/chat`, and formatting a strict JSON body, the SDK functions as a automated HTTP client wrapper.

When you write this:

```javascript
ollama.chat({ model: 'qwen2.5:3b', messages: messages })

```

The source code of the `ollama` library translates that simple object into this exact HTTP lifecycle automatically:

* It spins up an asynchronous network client (like `fetch` or `axios`).
* It targets the default endpoint: `POST http://localhost:11434/api/chat`
* It converts your javascript variable structure into a standardized, raw JSON body payload.
* It sends the request, waits for the response stream, and formats the output into clean data variables you can use.

### When *would* you need to use Route Handlers or Thunder Client?

You will bring those tools back into the mix the second you decide to wrap this into your own application architecture (like a full-stack MERN or Express app).

For example, if you wanted to build a custom chat app website where a frontend user could talk to your local model:

1. You would write your own **Express route handler** (e.g., `router.post('/my-chat-bot')`).
2. Inside *your* route handler, your server code would use the `ollama` SDK to talk to the local engine.
3. You would then use **Thunder Client** to test *your* Express backend endpoint (`http://localhost:5000/my-chat-bot`) to make sure your routing logic connects to the AI cleanly before writing your frontend UI.