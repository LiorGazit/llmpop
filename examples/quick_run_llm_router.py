# Quick run of LLM-Router:  
# -------
# Quickest on Colab (In Edit, pick the free `T4 GPU`), just copy and paste code.
# Make sure to install:
# pip -q install git+https://github.com/LiorGazit/llm_router.git 

from llm_router import init_llm, start_resource_monitoring
from langchain_core.prompts import ChatPromptTemplate

# Spinning up OpenAI's free GPT-OSS-20B, give it a few minutes, it's worth it.
# If you want a quick LLM, set model="llama3.2:1b".
model = init_llm(model="gpt-oss:20b", provider="ollama")
prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")
user_prompt = "What OS is better for deploying high scale programs in production? Linux, or Windows?"
print((prompt | model).invoke({"q":user_prompt}).content)