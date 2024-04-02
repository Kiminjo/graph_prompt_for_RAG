"""
This Python code is a code that tested the graph construction performance of diffbot, a type of graph RAG intersection in langchain.

Result:
No single entity and relationship was found.
The reason seems to be that we extract the main meaning using our own NLP model, not LLM model.
"""

from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer
from langchain_core.documents import Document

import os, sys 
from pathlib import Path 

import pandas as pd 
import yaml 

# Set system path and working dir 
os.chdir(str((Path(__file__).parent.parent)))
sys.path.append(str(Path(__file__).parent.parent))

# Read API Key
with open("data/api_info.yaml", "r") as f: 
    api_list = yaml.safe_load(f)
    f.close()
openai_api = api_list["OpenAI"]["API"]

# Get data 
script_paths = sorted([str(p) for p in Path("data/").glob("**/*.xlsx")])
target_script = script_paths[0]

script_table = pd.read_excel(target_script)
text = ""
for _, (character, converstaion) in script_table.iloc[3:, :].iterrows():
    text += f"{character}: {converstaion} \n"

# Transform text data to Doucment
documents = [Document(page_content=text)]

# Make graph using Diffbot
diffbot_api_key = "<YOUR_DIFFBOT_API_KEY>"
diffbot_nlp = DiffbotGraphTransformer(diffbot_api_key=diffbot_api_key)

graph_documents = diffbot_nlp.convert_to_graph_documents(documents)