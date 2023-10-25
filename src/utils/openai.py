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
    def __init__(self, api_key, sys_prompt:str="You are a helpful assistant"):
        openai.api_key = api_key
        self.api_key = api_key
        self.chat = Chat(sys_prompt=sys_prompt)
    
    def error_handler(f, *args, **kwargs):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                return e.args
        return wrapper

    def __detect_error(self, data):
        if data.get('error', None) != None:
            raise Exception(data['error']['type'], data['error']['message'])

    @error_handler
    def chat_with_gpt(self, question:str, model:str="gpt-3.5-turbo", max_tokens:int=2048, max_n:int=10, stream=False):
        conn = http.client.HTTPSConnection("api.openai.com")
        context = self.chat.to_prompt(max_n=max_n)
        new_message = Message(role="user", content=question)
        context.append(new_message.to_prompt())
        payload = json.dumps({
        "model": model,
        "messages": context,
        "max_tokens": max_tokens,
        "stream": stream
        })
        headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/chat/completions", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        if stream:
            temp = data.split("\n")
            ret = ""
            print(data)
            for i in temp:
                self.__detect_error(json.loads(i.split(':', maxsplit=1)[-1]))
                if i.startswith('data: {'):
                    delta:dict = json.loads(i.split(':', maxsplit=1)[-1])['choices'][0]['delta']
                    if delta.get('content', None) != None:
                        ret += delta['content']
            
            self.chat.add_message(new_message)
            self.chat.add_message(Message(role="assistant", content=ret))
            return ret
        else:
            json_data = json.loads(data)
            self.__detect_error(json_data)
            message = json_data['choices'][-1]['message']
            ret = message['content']
            self.chat.add_message(new_message)
            self.chat.add_message(Message(role="assistant", content=ret))
            return ret
    
    @error_handler
    def complete(self, prompt:str, model:str="text-davinci-003", max_tokens:int=2048, stop:str="", stream:bool=False):
        conn = http.client.HTTPSConnection("api.openai.com")
        payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0,
        "top_p": 1,
        "n": 1,
        "stream": stream,
        "logprobs": None,
        "stop": stop
        })
        headers = {
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/completions", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        self.__detect_error(json_data)
        return json_data['choices'][0]['text']

    @error_handler
    def edit(self, input_text:str, instruction:str, model:str="text-davinci-edit-001"):
        conn = http.client.HTTPSConnection("api.openai.com")
        payload = json.dumps({
        "model": model,
        "input": input_text,
        "instruction": instruction
        })
        headers = {
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/edits", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        self.__detect_error(json_data)
        return json_data['choices'][0]['text']
    
    @error_handler
    def text_to_image(self, prompt:str, n:int=1, size:str="1024x1024"):
        """Generate image from text prompt

        Args:
            prompt (str): description of image
            n (int, optional): number of images to generate. Defaults to 1.
            size (str, optional): size of generated image. Defaults to "1024x1024", only support 256, 512 and 1024.
        """
        conn = http.client.HTTPSConnection("api.openai.com")
        payload = json.dumps({
        "prompt": prompt,
        "n": n,
        "size": size
        })
        headers = {
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/images/generations", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        self.__detect_error(json_data)
        images = [i['url'] for i in json_data['data']]

        return images
    
    @error_handler
    def embedding(self, input_text:str, model:str="text-embedding-ada-002"):
        """Get vector embedding of text

        Args:
            input_text (str): the text to embed
            model (str, optional): model to use. Defaults to "text-embedding-ada-002".
        """

        conn = http.client.HTTPSConnection("api.openai.com")
        payload = json.dumps({
        "model": "text-embedding-ada-002",
        "input": input_text
        })
        headers = {
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/embeddings", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        self.__detect_error(json_data)
        return json_data['data'][0]['embedding']
    
    @error_handler
    def moderation(self, input_text:str):
        """Classify text as safe or toxic

        Args:
            input_text (str): the text to classify
        """
        conn = http.client.HTTPSConnection("api.openai.com")
        payload = json.dumps({
        "input": input_text
        })
        headers = {
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/moderations", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        self.__detect_error(json_data)
        return json_data['results']
    
    @error_handler
    def audio_to_text(self, file_path:str, language:str="en"):
        audio_file= open(file_path, "rb")
        conn = http.client.HTTPSConnection("api.openai.com")
        payload = json.dumps({
        "file": audio_file.read(),
        "model": "whisper-1",
        "language": language
        })
        headers = {
        'Authorization': f'Bearer {self.api_key}',
        }
        conn.request("GET", "/v1/files/", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        self.__detect_error(json_data)
        return json_data['text']
