from fastapi import FastAPI
from pydantic import BaseModel
from src.utils.load_config import LoadConfig
from src.utils.app_utils import Apputils

APPCFG = LoadConfig()
app = FastAPI(title="WebSearch API", description="Simple FastAPI backend")

class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_input = request.user_input
    messages = [
        {"role": "system", "content": str(APPCFG.llm_function_caller_system_role)},
        {"role": "user", "content": f"# User new question:\n {user_input}"}
    ]
    try:
        first_llm_response = Apputils.ask_llm_function_caller(
            gpt_model=APPCFG.gpt_model,
            temperature=APPCFG.temperature,
            messages=messages,
            function_json_list=Apputils.wrap_functions()
        )

        msg = first_llm_response.choices[0].message.tool_calls
        if msg is not None:
            try:
                web_search_result = Apputils.execute_json_function(first_llm_response)
                web_search_results = f"\n\n# Web search results:\n{str(web_search_result)}"
                messages = [
                    {"role": "system", "content": APPCFG.llm_system_role},
                    {"role": "user", "content": web_search_results + f"\n# User new question:\n {user_input}"}
                ]
                second_llm_response = Apputils.ask_llm_chatbot(APPCFG.gpt_model, APPCFG.temperature, messages)
                return {"response": second_llm_response.choices[0].message.content}
            except Exception as e:
                print(e)
                return {"response": "An error occurred with the function calling, please try again later."}
        else:
            try:
                return {"response": first_llm_response.choices[0].message.content}
            except Exception as e:
                print(e)
                return {"response": "An error occurred, please try again later."}
    except Exception as e:
        print(e)
        return {"response": "An internal error occurred."}

@app.get("/")
def read_root():
    return {"message": "WebSearch API is running"}
