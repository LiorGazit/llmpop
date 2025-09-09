# Quick run of LLMPop:  
# -------
# Quickest on Colab (In Edit, pick the free `T4 GPU`), just copy and paste code.
# Make sure to install:
# pip -q install llmpop 

from llmpop import init_llm, start_resource_monitoring
from langchain_core.prompts import ChatPromptTemplate

# Start with Meta's Llama. If you want a stronger (and bigger) model, try OpenAI's free "gpt-oss:20b":
model = init_llm(model="llama3.2:1b", provider="ollama")
prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")
user_prompt = "What OS is better for deploying high scale programs in production? Linux, or Windows?"
print((prompt | model).invoke({"q":user_prompt}).content)