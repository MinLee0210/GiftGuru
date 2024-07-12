import os
from dotenv import load_dotenv

from giftguru.mindsdb.setup_mindsdb import MindsDBServer
from giftguru.mindsdb.agent import MindsAgent

from utils import yaml_read
load_dotenv()

config = yaml_read('./config.yaml')
minds_config = config['mindsdb']
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if __name__ == "__main__": 
    mindsdb_server = MindsDBServer(config=minds_config)
    minds_agent = MindsAgent(server=mindsdb_server, 
                             config=minds_config, 
                             api_key=GEMINI_API_KEY)
    
    prompt = "What is the weather today?"
    result = minds_agent.run(input=prompt)
    print(result)