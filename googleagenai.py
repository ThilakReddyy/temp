from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

template = "You are Maya, an AI assiatant who provides throughful and helpful responses"

model = ChatGoogleGenerativeAI(model="gemini-pro", api_key=api_key)
prompt = ChatPromptTemplate.from_template(template)


chain = prompt | model
user_input = input("saay something")
response = chain.invoke({"user_input": user_input})
print(response.content)
