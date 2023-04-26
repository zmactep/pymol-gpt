"""Runs all requests to OpenAI"""
import openai
from pymol import cmd

from .config import MODELS

SYSTEM_PROMPT = "You are an AI integrated to PyMOL software. You will get a current status of PyMOL objects and a request. Your task is to translate the request into related pymol commands. Do not answer anything except these commands."

def send_request(request, config):
    """Send response"""
    openai.api_key = config['api_key']

    structures = cmd.get_names('objects')
    selections = cmd.get_names('selections')
    groups = cmd.get_names('group_objects')

    user_prompt = f"In the current state PyMOL has {len(structures)} stuctures {structures if structures else ''}, {len(selections)} selections {selections if selections else ''} and {len(groups)} groups {groups if groups else ''}. The request is: {request}."

    content = None
    try:
        response = openai.ChatCompletion.create(model=MODELS[config['model']], messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_prompt}
        ])
    except Exception:
        return content
    content = response['choices'][0]['message']['content']
    return content

def run_response(response):
    """Runs response as a command"""
    cmd.do(response)
