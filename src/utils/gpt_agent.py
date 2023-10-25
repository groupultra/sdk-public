import openai
import os
import http.client
import json

class Message:
        role: str
        content: str
        def __init__(self, role:str, content:str):
            self.role = role
            self.content = content

        def to_prompt(self):
            return {
                "role": self.role,
                "content": self.content
            }
class Chat():
    def __init__(self, sys_prompt:str="You are a helpful assistant"):
        self.context:[Message] = [Message(role="system", content=sys_prompt)]
    def add_message(self, role, content):
        self.context.append(Message(role=role, content=content))

    def add_message(self, message:Message):
        self.context.append(message)
    
    def to_prompt(self, max_n:int=10):
        if len(self.context) > max_n:
            ret = [self.context[0].to_prompt()]
            ret += [i.to_prompt() for i in self.context[-max_n:]]
        else:
            ret = [i.to_prompt() for i in self.context]
        return ret

class OpenAI():
    def __init__(self, api_key):
        openai.api_key = api_key
        self.api_key = api_key
        self.chat = Chat()
    
    def chat_with_gpt(self, question:str, model:str="gpt-3.5-turbo", max_tokens:int=8192, max_n:int=10):
        conn = http.client.HTTPSConnection("api.openai.com")
        context = self.chat.to_prompt(max_n=max_n)
        new_message = Message(role="user", content=question)
        context.append(new_message.to_prompt())
        payload = json.dumps({
        "model": model,
        "messages": context,
        "stream": True
        })
        headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/chat/completions", payload, headers)
        res = conn.getresponse()
        data = res.read()
        temp = data.decode("utf-8").split("\n")
        ret = ""
        print(data)
        for i in temp:
            if i.startswith('data: {'):
                delta:dict = json.loads(i.split(':', maxsplit=1)[-1])['choices'][0]['delta']
                if delta.get('content', None) != None:
                    ret += delta['content']
        
        self.chat.add_message(new_message)
        self.chat.add_message(Message(role="assistant", content=ret))
        return ret