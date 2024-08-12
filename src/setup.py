from setuptools import setup

setup(
    name='moobius',
    version='1.4.6',
    description='Moobius SDK',
    packages=['moobius'],
    #scripts=['bin/moobius.cmd'], #https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    entry_points={"console_scripts": ["moobius = moobius.quickstart:save_starter_ccs"]}, #https://stackoverflow.com/questions/774824/explain-python-entry-points
    install_requires=[
        'requests',
        'aioprocessing',
        'aiohttp',
        'APScheduler',
        'dacite',
        'redis',
        'websockets',
        'loguru',
    ],
)
