import requests
import json
from langchain_community.chat_models.friendli import ChatFriendli
import deepl
url = "https://suite.friendli.ai/api/beta/retrieve"

PAT = "flp_OydC1Y4tVFBfs1cgI5u0h9bUkQnNDrROcj3ARS751k083"

payload = json.dumps({
  "query": "Give me 5 multiple choice questions",
  "k": 13,
  "document_ids": ["3u69DmLLf5Hb"]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {PAT}'
}

response = requests.request("POST", url, headers=headers, data=payload)
response = response.json()
contexts = [r["content"] for r in response["results"]]

llm = ChatFriendli(
    model="meta-llama-3-70b-instruct", friendli_token="flp_OydC1Y4tVFBfs1cgI5u0h9bUkQnNDrROcj3ARS751k083"
)


template = """When we ask you to create a problem, write down the keyword "problem" as it is, don't write down the number of the problem, but don't use the keyword "1" in "problem 1", and then write down the problem with a double space next to it. This should be on a single line, and make sure to put two spaces between the problem and the problem description so that it's separated by a split (" "). When we ask you to create a question, we don't want any additional answers except for the part that is relevant to the question (ex: Yes, I understand) and never give a question with multiple answers, only one correct answer. When we ask you to create multiple questions, you must print '----------------' between the question and the question, and nothing else, either space or enter. All questions should be at the level of a first or second year undergraduate student, and at a level that will help them understand their major. And for multiple choice questions, make the answer very clear. I'll give you $30 if you do a good job.
{context}

Question: {question}

Helpful Answer:"""

rag_message = template.format(
    context="\n".join(contexts), question='''I need you to create 4 multiple choice questions based on the official C++ documentation template. The questions must have a blank space like '____', which you must fill in with the correct answer. Example 1) In Java, _____ is a keyword used to inherit a parent class. Example 2) In C++, the destructor uses the keyword ___. Example 3) In Python, _____ is a data structure that uses hash values to store values. And you can only give 4 choices, and each choice must have a keyword such as 1.) to separate the order.) And you can separate the question, the options, the answer, and everything else with an enter, and the options should take up one line per option, and the answer should be right below the multiple choice options.) And there must be only one correct answer, so don't ask questions about examples because you can't use them as a reference. I will run the ex(specific class or method name) translator, so don't answer questions with characters that break when running the translator. The most important thing is to respect the constraints I put in place when printing the problem. remove all markdown i want text only. no number state in individual problem, only 'problem' we want'''
)
auth_key = "44c49157-0a84-4b83-954f-1b9125baf794:fx"
translator = deepl.Translator(auth_key)

message = llm.call_as_llm(message=rag_message)
result = translator.translate_text(message, target_lang="KO")
from openai import OpenAI # openai==1.2.0

client = OpenAI(
  api_key="up_n76I9G4SKzOq3N463RI0V2x3r7d6n",
  base_url="https://api.upstage.ai/v1/solar"
)
content = message

stream = client.chat.completions.create(
  model="solar-1-mini-translate-enko",
  messages=[
    {
      "role": "system",
      "content": "You are a translation assistant that translates English to Korean."
    },
    {
      "role": "user",
      "content": content
    }
  ],
  stream=True,
)

rtr = ''
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        rtr += chunk.choices[0].delta.content
print(rtr)