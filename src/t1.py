print("ddd")
import os
import openai
openai.organization = "org-ahAnBcJ8PEbntuLXhBT35PIe"
openai.api_key = os.getenv("OPEN_API_KEY")
print(openai.Model.list())