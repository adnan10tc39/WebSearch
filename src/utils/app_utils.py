from typing import Dict
import inspect
import json
from inspect import Parameter
from pydantic import create_model
from src.utils.web_search import WebSearch
from typing import List, Dict
# import openai
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


class Apputils:
    @staticmethod
    def jsonschema(f) -> Dict:
        kw = {
            n: (o.annotation, ... if o.default == Parameter.empty else o.default)
            for n, o in inspect.signature(f).parameters.items()
        }
        model = create_model(f'Input for `{f.__name__}`', **kw)
        # pydantic v1 vs v2
        try:
            params = model.model_json_schema()   # v2
        except Exception:
            params = model.schema()              # v1

        return {
            "type": "function",
            "function": {
                "name": f.__name__,
                "description": f.__doc__ or "",
                "parameters": params,
            }
        }

    @staticmethod
    def wrap_functions() -> List[Dict]:
        return [
            Apputils.jsonschema(WebSearch.retrieve_web_search_results),
            Apputils.jsonschema(WebSearch.web_search_text),
            Apputils.jsonschema(WebSearch.web_search_pdf),
            Apputils.jsonschema(WebSearch.get_instant_web_answer),
            Apputils.jsonschema(WebSearch.web_search_image),
            Apputils.jsonschema(WebSearch.web_search_video),
            Apputils.jsonschema(WebSearch.web_search_news),
            Apputils.jsonschema(WebSearch.web_search_map),
        ]

    @staticmethod
    def execute_json_function(response) -> List:
        # func_name=response.choices[0].message.tool_calls[0].function.name
        # func_args=response.choices[0].message.tool_calls[0].function.arguments
        func_name: str = response.choices[0].message.tool_calls[0].function.name
        func_args: Dict = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

        # print("final argumanets", func_args)

        if func_name == 'retrieve_web_search_results':
            return WebSearch.retrieve_web_search_results(**func_args)
        elif func_name == 'web_search_text':
            return WebSearch.web_search_text(**func_args)
        elif func_name == 'web_search_pdf':
            return WebSearch.web_search_pdf(**func_args)
        elif func_name == 'web_search_image':
            return WebSearch.web_search_image(**func_args)
        elif func_name == 'web_search_video':
            return WebSearch.web_search_video(**func_args)
        elif func_name == 'web_search_news':
            return WebSearch.web_search_news(**func_args)
        elif func_name == 'get_instant_web_answer':
            return WebSearch.get_instant_web_answer(**func_args)
        elif func_name == 'web_search_map':
            return WebSearch.web_search_map(**func_args)
        else:
            raise ValueError(f"Function '{func_name}' not found.")


    @staticmethod
    def ask_llm_function_caller(gpt_model: str, temperature: float, messages: List, function_json_list: List):
        """
        Generate a response from an OpenAI ChatCompletion API call with specific function calls.

        Parameters:
            gpt_model (str): The name of the GPT model to use.
            temperature (float): The temperature parameter for the API call.
            messages (List): List of message objects for the conversation.
            function_json_list (List): List of function JSON schemas.

        Returns:
            The response object from the OpenAI ChatCompletion API call.
        """
        
        response = client.chat.completions.create(
            model=gpt_model,
            messages=messages,
            tools=function_json_list,
            tool_choice="auto",
            temperature=temperature
        )
        return response

    @staticmethod
    def ask_llm_chatbot(gpt_model: str, temperature: float, messages: List):
        """
        Generate a response from an OpenAI ChatCompletion API call without specific function calls.

        Parameters:
            gpt_model (str): The name of the GPT model to use.
            temperature (float): The temperature parameter for the API call.
            messages (List): List of message objects for the conversation.

        Returns:
            The response object from the OpenAI ChatCompletion API call.
        """
   
        response = client.chat.completions.create(
            model=gpt_model,
            messages=messages,
            temperature=temperature
        )
        return response
