"""
This Python code is a reproduction of the graph construction process provided by langchain.

Please refer to the link below for a detailed explanation of the code.

Result:
As a result of constructing the knowledge graph through this code, it was confirmed that the graph was generated too simply.

This is confirmed by the fact that the generation prompt of the graph transformer used to build the graph states the following.
- sacrifing accuracy. Do not add any information that is not explicitly
- he aim is to achieve simplicity and clarity in the knowledge graph, making it

Problems:
- The graph module provided by langchain depends on neo4j.
- In order to use this neo4j module, there is a problem that its own SQL language must be entered as a prompt.

It is necessary to build a knowledge graph by building LLM on its own.
"""

from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
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

# Set neo4j graph 
os.environ["NEO4J_URI"] = "<YOUR_NEO4J_URI>"
os.environ["NEO4J_USERNAME"] = "<YOUR_NEO4J"
os.environ["NEO4J_PASSWORD"] = "<YOUR_NEO4J_PASSWORD>"

graph = Neo4jGraph()

# Preprare instance for construct graph DB 
llm = ChatOpenAI(temperature=0, 
                 model_name="gpt-4-0125-preview", 
                 openai_api_key=openai_api)
llm_transformer = LLMGraphTransformer(llm=llm,
                                    #   allowed_relationships=["REPAIRED", "HELPED", "THANKED", "SAVED", "DANGERED"])
                                      )

# Get data 
script_paths = sorted([str(p) for p in Path("data/").glob("**/*.xlsx")])
target_script = script_paths[0]

script_table = pd.read_excel(target_script)
text = ""
for _, (character, converstaion) in script_table.iloc[3:, :].iterrows():
    text += f"{character}: {converstaion} \n"

# Make document file 
documents = [Document(page_content=text)]
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")  
graph.add_graph_documents(graph_documents)

# Inference using graph 
infer_llm = ChatOpenAI(temperature=0, 
                       model_name="gpt-4-0125-preview", 
                       openai_api_key=openai_api)
chain = GraphCypherQAChain.from_llm(
    graph=graph, llm=llm, exclude_types=["Genre"], verbose=True
)
print("here")
