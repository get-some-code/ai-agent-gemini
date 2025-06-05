# 🤖 AI Agent — Powered by Gemini API

Welcome to your very own **AI Agent** project! This is a powerful assistant built using Google's **Gemini 1.5 Flash** model. It can reason, take actions, write files, run commands, and simulate multi-step planning just like an intelligent agent.

---

## 🚀 Features

- 🧠 **Chain-of-Thought Reasoning**
- 🛠️ **Tool Usage** (like `write_file`, `run_command`, etc.)
- 💬 **Interactive Terminal Chat**
- 🔍 **JSON Parsing** for structured agent responses
- 📁 **File System Integration** for smart folder & file management
- 🧪 **Agent Memory** using chat history
- 🔗 **Ready to push to GitHub**

## 🛠️ Supported Tools

| Tool Name      | Description                                                                 | Input Type           | Example Usage                                  |
|----------------|-----------------------------------------------------------------------------|----------------------|------------------------------------------------|
| run_command    | Executes terminal/command-line commands (cross-platform supported).         | str (command)        | "mkdir my_project"                             |
| write_file     | Writes content to a file at the specified path.                             | dict                 | {"path": "test.txt", "content": "Hello"}       |
| read_file      | Reads content from a file and returns its text.                             | str (file path)      | "README.md"                                    |
| check_exists   | Checks if a file or folder exists in the current working directory.         | str (path)           | "todo-app/src/App.jsx"                         |
| get_weather    | Fetches current weather for a given city (via API or mock setup).           | str (city name)      | "Kolkata"                                      |
| list_dir       | Lists all files and folders inside a given directory.                       | str (folder path)    | "todo-app/src"                                 |

---

- You can add your own tools easily.
---

## 🤔 What is an AI Agent?

An **AI agent** is a system that:
- Understands goals from natural language.
- Plans the next actions.
- Executes tools to complete the task.
- Observes outcomes and adapts.

Think of it as a self-driving assistant that can **reason + act**, just like J.A.R.V.I.S. from Iron Man!

---

## 📦 Project Structure

```bash
AI Agent/
├── main.py                
├── system_prompt.txt    
├── README.md
└── .gitignore
```

##  Installation?
1. Clone the repo:
```
git clone https://github.com/get-some-code/ai-agent-gemini.git
```
```
cd ai-agent-gemini
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Set your Gemini API Key:
```
# in main.py
genai.configure(api_key="your_api_key_here")
```

## How It Works ?
- Chat Session
```
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
chat = model.start_chat(history=[ ... ])
```
- Parse AI Response
```
response = chat.send_message(user_input)
parsed_data = parse_input_string(response.text)
```
- Execute Tools Based on further Steps

## Demo Output:
``` 
You: create a folder calculator with an index.html file
🤖Assistant: 
▶ Start: User wants to create a calculator web app
💡 Plan: I will create folder & add HTML file
🚀 Action: Calling write_file tool!
👀 Observe: File written to calculator/index.html
🎯 Final Output: All done! Your calculator folder is ready.
```


Watch the demo video of the Gemini AI Agent in action:

🔗 [View Demo on Google Drive](https://drive.google.com/file/d/1iOZnObB2rRItsH4sWzig14OeNd8yAJ35/view?usp=sharing)


