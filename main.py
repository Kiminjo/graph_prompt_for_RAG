from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

import os, sys 
from pathlib import Path

import pandas as pd 
import yaml

from prompt_for_KG import system_prompt

# Set system path and working dir 
os.chdir(str((Path(__file__).parent)))
sys.path.append(str(Path(__file__).parent))

# Read API Key
with open("data/api_info.yaml", "r") as f: 
    api_list = yaml.safe_load(f)
    f.close()
openai_api = api_list["OpenAI"]["API"]

# Preprare instance for construct graph DB 
llm = ChatOpenAI(temperature=0, 
                 model_name="gpt-4-0125-preview", 
                 openai_api_key=openai_api)

default_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        (
            "human",
            (
                "Tip: Make sure to answer in the correct format and do "
                "not include any explanations. "
                "Use the given format to extract information from the "
                "following input: {input}"
            ),
        ),
    ]
)

chain = default_prompt | llm

# Get data 
script_paths = sorted([str(p) for p in Path("data/").glob("**/*.xlsx")])
target_script = script_paths[3]

script_table = pd.read_excel(target_script)
text = ""
for _, (character, converstaion) in script_table.iloc[3:, :].iterrows():
    text += f"{character}: {converstaion} \n"

# Make document file 
documents = [Document(page_content=text)]

# Get the result
result = chain.invoke(documents)
print(result)
print("here")