import aiohttp
import asyncio
import json
import openai
import tiktoken
from functools import reduce
from tenacity import retry, stop_after_attempt, wait_fixed

from .api_key import api_key
openai.api_key = api_key 

# load config
with open('config.json', 'r') as f:
    conf = json.load(f)

#!/usr/bin/env python3.8
class Obj(dict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Obj(b) if isinstance(b, dict) else b)


def dict_2_obj(d: dict):
    return Obj(d)


class HttpException(Exception):
    def __init__(self, msg):
        self.msg = msg

async def post_request(url, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, **kwargs) as resp:
            try:
                response = await resp.json()
                if resp.ok:
                    return response
                else:
                    raise HttpException(response)
            except aiohttp.ContentTypeError:
                return await resp.text()

async def get_request(url, headers={}):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            response = await resp.json()
            if resp.ok:
                return response
            else:
                raise HttpException(response)

async def patch_request(url, json_data, headers={}):
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=json_data, headers=headers) as resp:
            try:
                response = await resp.json()
                if resp.ok:
                    return response
                else:
                    raise HttpException(response)
            except aiohttp.ContentTypeError:
                return await response.text()

async def put_request(url, json_data, headers={}):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=json_data, headers=headers) as resp:
            try:
                response = await resp.json()
                if resp.ok:
                    return response
                else:
                    raise HttpException(response)
            except aiohttp.ContentTypeError:
                return await response.text()

class ProxyError(Exception):
    pass


async def get_answer(messages, use_proxy=False, model="gpt-4-0314"):
    try:
        response = await completion(use_proxy=use_proxy, messages=messages, temperature=1, max_tokens=1000, model=model)
        
        if 'err_msg_soc' in response:
            response = f"人设崩了，很可能是超出长度限制了！\n\n{response['err_msg_soc']}\n\n请发送【设定 人设内容】重新设定一下吧！"
        else:
            response = response['choices'][0]['message']['content']

    except openai.error.APIError as e:
        response = f"OpenAI API returned an API Error: {e}"

    except openai.error.RateLimitError as e:
        response = '问太多太快了，人家答不上来了！'
    
    except openai.error.Timeout as e:
        response = '人家脑慢了，一会儿再试试嘛！'

    except ProxyError as e:
        response = '代理田了！' + str(e)
    
    except Exception as e:
        response = '不知道为什么田了！\n\n' + str(e)

    finally:
        return response


async def get_answer_simple(text, use_proxy=False, model="gpt-4-0314"):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
    ]

    return await get_answer(messages, use_proxy=use_proxy, model=model)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
async def completion(use_proxy=False, **kwargs):
    if not 'model' in kwargs:
        kwargs['model'] = "gpt-4-0314"
    
    """
    if use_proxy:
        url = "https://frog.4fun.chat/account/openai"
        # payload = {"model": "gpt-3.5-turbo", **kwargs}
        payload = {"model": "gpt-4", **kwargs}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise ProxyError(resp.status)
    """

    response = await openai.ChatCompletion.acreate(**kwargs)
    return response


# gpt session
class GPTSession:
    def __init__(self, model="gpt-4-0314", use_proxy=False):
        self.model = model
        self.encoder = tiktoken.encoding_for_model(model)
        self.default_system = "You are a helpful assistant."
        default_token = self.calc_token(self.default_system)
        self.messages = [{
            "role": "system", 
            "content": self.default_system,
            "token": default_token
        }]
        self.max_token = 8192 if model.startswith('gpt-4') else 4096
        self.max_prompt_token = self.max_token - 1000 - default_token  # 留1000的回复token
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ]
        """
    
    def calc_token(self, text):
        return len(self.encoder.encode(text))
    
    # 设定
    def setting(self, text):
        tk = self.calc_token(text)
        if tk > self.max_token - 1000:
            return '不行不行，太长啦！'
        else:
            self.messages[0] = {
                "role": "system", 
                "content": text,
                "token": tk
            }
            return f'好奥！这个设定有{tk}token辣么多！'
    
    # 如果太长，自动从前面开始扔
    # 只需发送用户新增的话
    async def ask(self, text):
        text_token = self.calc_token(text)
        if text_token > self.max_prompt_token:
            return f'太几把长了！最多{self.max_prompt_token}token，你{text_token}token！'
        # 在message后面续一段
        self.messages.append({'role': 'user', 'content': text, 'token': text_token})
        # 计算token，如果超了开始仍
        total = sum([m['token'] for m in self.messages[1:]])
        while total > self.max_prompt_token:
            total -= self.messages[1]['token']
            self.messages = [self.messages[0]] + self.messages[2:]
        # 返回最新回复
        msg = [{'role': m['role'], 'content': m['content']} for m in self.messages]
        answer = await get_answer(msg, model=self.model)
        ans_token = self.calc_token(answer)
        self.messages.append({'role': 'assistant', 'content': answer, 'token': ans_token})
        # 添加价格信息
        if self.model.startswith('gpt-4'):
            price = (total + self.messages[0]['token']) / 1000 * 0.003 + ans_token / 1000 * 0.006
            return answer + f'\n{total + self.messages[0]["token"] + ans_token}token,${price:.4f}.'
        else:
            return answer

        
def get_botname_by_appid(appid):
    for k, v in conf['bots'].items():
        if v['app_id'] == appid:
            return v['name']
    return 'undefined'


# 判断一个字符串是否是正整数
def is_positive_integer(s):
    try:
        num = int(s)
        if num > 0:
            return True
        else:
            return False
    except ValueError:
        return False


# 数据库查询的包皮 返回所有
# 只支持等号儿和与运算
# 例：User.find((User.user_id == '123') & (User.name == '屎')).all()
# 可简化为：rgetall(User, user_id='123', name='屎')
def rgetall(cls, **kw):
    conds = [getattr(cls, k) == v for k, v in kw.items()]
    entry = cls.find(reduce(lambda x,y: x&y, conds)).all()
    return entry

# 数据库查询的包皮，只返回第一个结果儿，没有返回None
def rget(cls, **kw):
    entry = rgetall(cls, **kw)
    if entry:
        return entry[0]
    else:
        return None

