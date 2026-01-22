# LangChain Flow

## 0. Virtual Enviroment

```bash
    py -m venv [.name_of_virtual_environment]
    .\[.name_of_virtual_environment]\Scripts\Activate.ps1
    python -m pip install --upgrade pip
```

## 1. Install dependecies

```bash
    pip install langchain langchain-openai python-dotenv
```

## 2. Set OpenAI API Key

Create a `.env` file in the root directory of your project and add your OpenAI API key:

```env  
    OPENAI_API_KEY=your_openai_api_key_here
```

## 3. Develop your application

Create a Python file (e.g., `app.py`) and start coding with LangChain

## 4. Run your application

```bash
    python app.py
```