from setuptools import setup

setup(
    name='moobius',
    version='0.0.1',
    description='Moobius SDK',
    packages=['moobius'],
    install_requires=[
        'requests',
        'aioprocessing',
        'aiohttp',
        'APScheduler',
        'dacite',
        'openai',
        'redis',
        'websockets',
        'loguru',
    ],
)