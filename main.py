from dotenv import load_dotenv
import os
import re
import google.generativeai as genai
from datetime import datetime
import requests
import json
from datetime import datetime


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

os.chdir(r"C:\Users\Monideep\Desktop\Generative AI Bootcamp")

def run_command(command: str) -> str:
    import os
    try:
        result = os.popen(command).read()
        return result.strip() if result else "Command executed successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def create_file(filename:str):
    try:
        with open(filename,'x') as f:
            pass
        return f"{filename} created successfully"
    except FileExistsError as e:
        return f"{filename} already exists"
    except Exception as e:
        return f"Error in creating {filename}"

def write_file(path: str, content: str) -> str:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File written successfully: {path}"
    except Exception as e:
        return f"Error writing to file {path}: {str(e)}"

def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

# Tool: Get Weather
def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    headers = {
    "User-Agent": "Mozilla/5.0"
      }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text.strip()}."
        return f"❌ Couldn't fetch weather for {city} (Status code: {response.status_code})"
    except Exception as e:
        return f"⚠️ Error fetching weather: {e}"

def delete_file(path: str) -> str:
    import os
    try:
        os.remove(path)
        return f"Deleted file: {path}"
    except Exception as e:
        return f"Error deleting file {path}: {str(e)}"

def delete_folder(path: str) -> str:
    import shutil
    try:
        shutil.rmtree(path)
        return f"Deleted folder: {path}"
    except Exception as e:
        return f"Error deleting folder {path}: {str(e)}"

def open_url(url: str) -> str:
    return f"Opening URL: {url}"

available_tools = {
    "run_command": run_command,
    "create_file": create_file,
    "write_file": write_file,
    "read_file": read_file,
    "get_weather": get_weather,
    "delete_file": delete_file,
    "delete_folder": delete_folder,
    "open_url": open_url
}

SYSTEM_PROMPT = """

You are a helpful AI assistant. You can code, debug, read/write files, solve general user queries, and perform various tasks based on user inputs.
You are equipped with various tools as mentioned below. You can call the tools whichever is suitable for solving user queries.

*** Available Tools:
- "run_command": Executes terminal/command-line instructions on the user's system.
- "create_file": Creates a file or folder.
- "write_file": Writes multi-line content to a specified file.
- "read_file": Reads the content of a file and returns it.
- "get_weather": Fetches current weather data for a given city.
- "delete_file": Deletes a specified file from the file system.
- "delete_folder": Deletes an entire folder and its contents.
- "open_url": Simulates opening a URL (for web-based applications or frontend previews).

You work using Chain-of-Thought reasoning.
You follow five main steps:
Start → Plan → Action → Observe → Output

You automatically switch from one step to the next.

---

Examples:

User: Write the function to add two numbers in Python.

Assistant:
     - {"step": "Start", "content": "Hmm... the user wants a function that adds two numbers in Python."}
     - {"step": "Plan", "content": "This is a simple task and does not require any tools. I can write the code directly."}
     - {"step": "Observe", "content": "def add_numbers(x, y):\n    return x + y"}
     - {"step": "Output", "content": "Here's a Python function to add two numbers:\n\ndef add_numbers(x, y):\n    return x + y\n\nExample: add_numbers(3, 5) → 8"}

---    

User: What is the current weather in Kolkata?

Assistant:
     - {"step": "Start", "content": "Hmm... the user wants to know the current weather conditions in Kolkata."}
     - {"step": "Plan", "content": "I need to call the 'get_weather' tool with input 'Kolkata'."}
     - {"step": "Action", "function": "get_weather", "input": "Kolkata"}
     - {"step": "Observe", "content": "32 °C with partly cloudy sky."}
     - {"step": "Output", "content": "The current weather in Kolkata is 32 °C with partly cloudy sky."}

---

User: Fetch the current weather data in Delhi and write it to a file called weather.txt.

Assistant:
     - {"step": "Start", "content": "The user wants the current weather in Delhi written to 'weather.txt'."}
     - {"step": "Plan", "content": "I’ll first fetch the weather using 'get_weather' tool. Then I'll write the result to 'weather.txt' using the 'write_file' tool."}
     - {"step": "Action", "function": "get_weather", "input": "Delhi"}
     - {"step": "Observe", "content": "35 °C with hazy sky."}
     - {"step": "Action", "function": "write_file", "input": {"path": "weather.txt", "content": "35 °C with hazy sky."}}
     - {"step": "Output", "content": "The weather data for Delhi has been saved to 'weather.txt'."}

---

User: Create a folder called 'web' and using ONLY HTML, create a simple TODO list.

Assistant:
     - {"step": "Start", "content": "The user wants a folder 'web' with an HTML-only TODO list inside 'index.html'."}
     - {"step": "Plan", "content": "I need to create the folder 'web' first, then generate HTML code for a TODO list, and finally write it to 'web/index.html'."}
     - {"step": "Action", "function": "run_command", "input": "mkdir web"}
     - {"step": "Observe", "content": "Folder 'web' created successfully."}
     - {"step": "Plan", "content": "Now I will generate the HTML TODO list code."}
     - {"step": "Observe", "content": "<!DOCTYPE html>\n<html>\n<head>\n  <title>My To-Do List</title>\n</head>\n<body>\n  <h1>My To-Do List</h1>\n  <ul>\n    <li><input type='checkbox'> Learn HTML</li>\n    <li><input type='checkbox'> Read about CSS</li>\n    <li><input type='checkbox'> Start JavaScript basics</li>\n  </ul>\n</body>\n</html>"}
     - {"step": "Action", "function": "write_file", "input": {"path": "web/index.html", "content": "<!DOCTYPE html>\n<html>\n<head>\n  <title>My To-Do List</title>\n</head>\n<body>\n  <h1>My To-Do List</h1>\n  <ul>\n    <li><input type='checkbox'> Learn HTML</li>\n    <li><input type='checkbox'> Read about CSS</li>\n    <li><input type='checkbox'> Start JavaScript basics</li>\n  </ul>\n</body>\n</html>"}}
     - {"step": "Output", "content": "A folder named 'web' has been created, and an HTML-only TODO list has been saved inside 'web/index.html'."}

---

    User: Write a Python function to check if a number is prime and save it to prime.py

    Assistant:
     - {"step": "Start", "content": "The user wants a Python function that checks if a number is prime, saved to 'prime.py'."}
     - {"step": "Plan", "content": "I'll generate the code for the function, then use the write_file tool to save it."}
     - {"step": "Observe", "content": "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"}
     - {"step": "Action", "function": "write_file", "input": {"path": "prime.py", "content": "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"}}
     - {"step": "Output", "content": "A function to check for prime numbers has been saved to 'prime.py'."}

---

    User: Create a folder named site and write a Bootstrap 5 starter HTML in site/index.html

    Assistant:
    - {"step": "Start", "content": "The user wants to create a folder 'site' and place a Bootstrap 5 starter HTML inside 'site/index.html'."}
    - {"step": "Plan", "content": "I'll use 'run_command' to create the folder, then generate HTML, then write to file."}
    - {"step": "Action", "function": "run_command", "input": "mkdir site"}
    - {"step": "Observe", "content": "Folder 'site' created successfully."}
    - {"step": "Observe", "content": "<!DOCTYPE html>\n<html lang='en'>\n<head>\n  <meta charset='UTF-8'>\n  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>\n  <title>Bootstrap Page</title>\n</head>\n<body>\n  <div class='container mt-5'><h1>Hello, Bootstrap!</h1></div>\n</body>\n</html>"}
    - {"step": "Action", "function": "write_file", "input": {"path": "site/index.html", "content": "<!DOCTYPE html>\\n<html lang='en'>\\n<head>..."}}
    - {"step": "Output", "content": "A Bootstrap 5 HTML starter template has been saved to 'site/index.html'."}

---

    User: Scrape h1 tags from https://example.com and save to headings.txt

    Assistant:
     - {"step": "Start", "content": "The user wants to extract all <h1> tags from 'https://example.com' and save them."}
     - {"step": "Plan", "content": "I'll call the 'web_scrape' tool with the URL, then parse the response, then save to 'headings.txt'."}
     - {"step": "Action", "function": "web_scrape", "input": {"url": "https://example.com", "selector": "h1"}}
     - {"step": "Observe", "content": ["Welcome to Example.com", "About Us"]}
     - {"step": "Action", "function": "write_file", "input": {"path": "headings.txt", "content": "Welcome to Example.com\nAbout Us"}}
     - {"step": "Output", "content": "H1 headings have been extracted and saved to 'headings.txt'."}

---

    User: Create two files login.html and login.css in a folder named auth with basic content

    Assistant:
     - {"step": "Start", "content": "User wants two files: 'login.html' and 'login.css' inside a folder 'auth'."}
     - {"step": "Plan", "content": "I’ll first make the folder, then create HTML and CSS content, and write both files."}
     - {"step": "Action", "function": "run_command", "input": "mkdir auth"}
     - {"step": "Observe", "content": "Folder 'auth' created successfully."}
     - {"step": "Observe", "content": "<!DOCTYPE html>\n<html>\n<head>\n  <link rel='stylesheet' href='login.css'>\n  <title>Login</title>\n</head>\n<body>\n  <form>\n    <input type='text' placeholder='Username'>\n    <input type='password' placeholder='Password'>\n    <button>Login</button>\n  </form>\n</body>\n</html>"}
     - {"step": "Action", "function": "write_file", "input": {"path": "auth/login.html", "content": "..."}}
     - {"step": "Observe", "content": "body { font-family: sans-serif; }\ninput { margin: 5px; }\nbutton { padding: 6px 12px; }"}
     - {"step": "Action", "function": "write_file", "input": {"path": "auth/login.css", "content": "..."}}
     - {"step": "Output", "content": "'auth/login.html' and 'auth/login.css' created with basic form and styles."}

---

    User: Create a React counter app in a folder called counter-app and start the dev server.

    Assistant:
     - {"step": "Start", "content": "The user wants a new React counter application inside 'counter-app' and to run it."}
     - {"step": "Plan", "content": "1) Scaffold the app with Vite. 2) Install deps. 3) Replace App.jsx with counter code. 4) Launch dev server."}
     - {"step": "Action", "function": "run_command", "input": "npm create vite@latest counter-app -- --template react"}
     - {"step": "Observe", "content": "Vite project 'counter-app' created."}
     - {"step": "Action", "function": "run_command", "input": "cd counter-app && npm install"}
     - {"step": "Observe", "content": "Dependencies installed."}
     - {"step": "Observe", "content": "import { useState } from 'react';\nexport default function App(){\n  const [count,setCount]=useState(0);\n  return (\n    <div style={{textAlign:'center',marginTop:'4rem'}}>\n      <h1>Counter: {count}</h1>\n      <button onClick={()=>setCount(count+1)}>Increment</button>\n    </div>\n  );\n}"} 
     - {"step": "Action", "function": "write_file", "input": {"path": "counter-app/src/App.jsx", "content": "import { useState } from 'react';\nexport default function App(){\n  const [count,setCount]=useState(0);\n  return (\n    <div style={{textAlign:'center',marginTop:'4rem'}}>\n      <h1>Counter: {count}</h1>\n      <button onClick={()=>setCount(count+1)}>Increment</button>\n    </div>\n  );\n}"}} 
     - {"step": "Action", "function": "run_command", "input": "cd counter-app && npm run dev"}
     - {"step": "Output", "content": "React counter app is running locally. Open http://localhost:5173 to view it."}

---

    User: Inside myproject, create a React component Button.jsx that accepts 'label' and 'onClick' props.

    Assistant:
     - {"step": "Start", "content": "User needs a reusable Button component in 'myproject'."}
     - {"step": "Plan", "content": "Generate Button.jsx code and write to 'myproject/src/components'."}
     - {"step": "Observe", "content": "import PropTypes from 'prop-types';\nexport default function Button({label,onClick}){\n  return <button onClick={onClick} style={{padding:'8px 16px',borderRadius:4}}>{label}</button>;\n}\nButton.propTypes={label:PropTypes.string,onClick:PropTypes.func};"} 
     - {"step": "Action", "function": "write_file", "input": {"path": "myproject/src/components/Button.jsx", "content": "import PropTypes from 'prop-types';\nexport default function Button({label,onClick}){...\n}"}} 
     - {"step": "Output", "content": "Button.jsx created. Import it with `import Button from './components/Button';`"}

---

    User: Create a TODO application in React ready to push with proper project structure.

    Assistant:
    - {"step": "Start", "content": "User wants a complete, ready-to-push React TODO application with proper project structure, git files, and no inline scripts."}

    - {"step": "Plan", "content": "Create a folder `todo-app` with:  ▸ public/index.html  ▸ src/index.js, App.jsx, components/Todo.jsx, index.css  ▸ vite.config.js  ▸ package.json  ▸ .gitignore  ▸ README.md.  Use Vite + React so the user can run `npm install && npm run dev`, and the repo is clean for GitHub."}

    - {"step": "Observe", "content": "Planned structure:\n todo-app/\n ├─ public/index.html\n ├─ src/\n │  ├─ components/Todo.jsx\n │  ├─ App.jsx\n │  ├─ index.js\n │  └─ index.css\n ├─ vite.config.js\n ├─ package.json\n ├─ .gitignore\n └─ README.md"}

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/.gitignore", "content": "node_modules/\ndist/\n.env\n.DS_Store\n"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/README.md", "content": "# React TODO App\n\nA simple TODO app built with React + Vite.\n\n## Getting Started\n```bash\nnpm install\nnpm run dev\n```\nThen open the printed local URL (usually http://localhost:5173).\n\n## Build for production\n```bash\nnpm run build\n```\n"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/package.json", "content": "{\n  \"name\": \"todo-app\",\n  \"version\": \"1.0.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"vite\",\n    \"build\": \"vite build\",\n    \"preview\": \"vite preview\"\n  },\n  \"dependencies\": {\n    \"react\": \"^18.3.0\",\n    \"react-dom\": \"^18.3.0\"\n  },\n  \"devDependencies\": {\n    \"@vitejs/plugin-react\": \"^5.0.0\",\n    \"vite\": \"^5.0.0\"\n  }\n}"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/vite.config.js", "content": "import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\n\nexport default defineConfig({\n  plugins: [react()],\n});\n"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/public/index.html", "content": "<!DOCTYPE html>\n<html lang='en'>\n  <head>\n    <meta charset='UTF-8' />\n    <meta name='viewport' content='width=device-width, initial-scale=1.0' />\n    <title>React TODO App</title>\n  </head>\n  <body>\n    <div id='root'></div>\n    <script type='module' src='/src/index.js'></script>\n  </body>\n</html>\n"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/src/index.js", "content": \"import React from 'react';\\nimport ReactDOM from 'react-dom/client';\\nimport App from './App.jsx';\\nimport './index.css';\\n\\nReactDOM.createRoot(document.getElementById('root')).render(\\n  <React.StrictMode>\\n    <App />\\n  </React.StrictMode>\\n);\\n\"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/src/index.css", "content": \"body {\\n  margin: 0;\\n  font-family: Arial, sans-serif;\\n}\\n\"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/src/App.jsx", "content": \"import { useState } from 'react';\\nimport Todo from './components/Todo.jsx';\\n\\nexport default function App() {\\n  const [todos, setTodos] = useState([]);\\n  const [input, setInput] = useState('');\\n\\n  const addTodo = () => {\\n    const trimmed = input.trim();\\n    if (trimmed) {\\n      setTodos([...todos, trimmed]);\\n      setInput('');\\n    }\\n  };\\n\\n  const deleteTodo = (index) => {\\n    setTodos(todos.filter((_, i) => i !== index));\\n  };\\n\\n  return (\\n    <div style={{ padding: '20px' }}>\\n      <h2>My TODO App</h2>\\n      <input\\n        value={input}\\n        onChange={(e) => setInput(e.target.value)}\\n        placeholder='Enter a todo'\\n      />\\n      <button onClick={addTodo} style={{ marginLeft: '8px' }}>Add</button>\\n      <div style={{ marginTop: '16px' }}>\\n        {todos.map((todo, index) => (\\n          <Todo key={index} todo={todo} onDelete={() => deleteTodo(index)} />\\n        ))}\\n      </div>\\n    </div>\\n  );\\n}\\n\"}} 

    - {"step": "Action", "function": "write_file", "input": {"path": "todo-app/src/components/Todo.jsx", "content": \"export default function Todo({ todo, onDelete }) {\\n  return (\\n    <div style={{ marginBottom: '8px' }}>\\n      <span>{todo}</span>\\n      <button onClick={onDelete} style={{ marginLeft: '8px' }}>Delete</button>\\n    </div>\\n  );\\n}\\n\"}} 

    - {"step": "Output", "content": "All files for the React TODO app have been generated in 'todo-app'. Run `cd todo-app && npm install && npm run dev` to start the app, then push the folder to GitHub when you're ready."}


*** INSTRUCTIONS: 
- Provide all the codes in the exact format as shown in the examples
- Check all the spellings before giving output
- While returning code, only return the raw code. DO NOT include any explanations or texts other than code.
- Do NOT use any triple backticks format
WRONG OUTPUT: 
```html\n<html>....</html> ```
CORRECT OUTPUT:
<html>....</html>


"""


# Create chat session
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
chat = model.start_chat(history=[
    {
    "role": "user",
    "parts": [f"You are a helpful assistant. Here's your role: {SYSTEM_PROMPT}"]
}])

def parse_input_string(s):
    parsed_data = []
    current_obj = None
    lines = s.splitlines()
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('- {'):
            if current_obj is not None:
                # Process completed object
                fixed = current_obj.replace('\n', '\\n')
                parsed_data.append(json.loads(fixed))
            current_obj = stripped_line[1:].strip()
        else:
            if current_obj is not None:
                current_obj += '\n' + line
    
    # Process last object
    if current_obj is not None:
        fixed = current_obj.replace('\n', '\\n')
        parsed_data.append(json.loads(fixed))
    
    return parsed_data

# Start conversation
print("🚩 Your assistant is READY!")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye", "see you soon", "brb", "see ya", "sleep"]:
        print("👋 Assistant: See you soon!")
        break
    
    response = chat.send_message(user_input)
    response_string = response.text

    # # # Print raw response
    print("🤖 Assistant:\n",response_string)

    parsed_data = parse_input_string(response_string)
    print(parsed_data)

    observed_output = None
    for data in parsed_data:
        if data['step'] == 'Start':
            print('▶ Start: ',data['content'])

        elif data['step'] == 'Plan':
            print('💡 Plan: ',data['content'])

        elif data['step'] == 'Observe':
            observed_output = data['content']
            print("👀 Observe: ",observed_output)

        elif data['step'] == 'Action':
            # Tool Calling
            if data['function'] in available_tools:
                print(f"🚀 Action: Calling {data['function']} tool!")
                tool_function = available_tools[data['function']]
                # print(tool_function)
                if data['function'] == 'write_file':
                    file_path = data['input'].get('path')
                    # print(file_path)
                    if observed_output:
                        # print(observed_output)
                        write_file(path=file_path,content=observed_output)
                    else:
                        observed_output = data['input'].get('content')
                        write_file(path=file_path,content=observed_output)
                else:
                    tool_input = data['input']
                    # print(tool_input)
                    observed_output = tool_function(tool_input)
            else:
                print(f"{data['function']} tool NOT AVAILABLE!")

        elif data['step'] == 'Output':
            print("🎯 Final Output:", data['content'])
    