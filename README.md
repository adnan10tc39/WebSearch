# Function calling and addressing the LLM knowledge cut-off with real-time web search using GPT models

**WebSearch** is a powerful tool enabling users to pose questions that require internet searches. Leveraging GPT models:
* It identifies and executes the most relevant given Python functions in response to user queries. 
* The second GPT model generates responses by combining user queries with content retrieved from the web search engine. 
* The web search supports diverse searches such as text, news, PDFs, images, videos, maps, and instant responses. 
* Overcoming knowledge-cutoff limitations, the chatbot delivers answers based on the latest internet content.


## Running the Project

To get the project up and running, you'll need to set up your environment and install the necessary dependencies. You can do this in two ways:

### Option 1: Using the Parent Directory Instructions
Activate your environment and run:
```
pip install -r requirements.txt
```


1. **Configuration and Execution**
* Navigate to the config directory.
* Create .env file add OPENAI_API_KEY=""
* Open Configs/app_confg.py and fill in your credentials.
2. **Activate Your Environment.**
3. **Ensure you are in the WebSearch directory**
4. **Run the API:**

In Terminal:

```
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```


