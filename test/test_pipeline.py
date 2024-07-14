import os 
import nest_asyncio
import random

from dotenv import load_dotenv

from giftguru.engines.scraper import ScrapeWebWorker
from giftguru.engines.search import TavilyWorker
from giftguru.mindsdb.server import MindsDBServer
from giftguru.mindsdb.agent import MindsAgent

from utils import yaml_read

load_dotenv()
nest_asyncio.apply()

config = yaml_read(dir='./config.yaml')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MINDSDB_API_KEY = os.getenv("MINDSDB_API_KEY")

search_config = config['engine']['search']
scraper_config = config['engine']['scraper']
minds_config = config['mindsdb']

tavily = TavilyWorker(api_key=TAVILY_API_KEY)
scraper = ScrapeWebWorker(config=scraper_config, 
                        api_key=MINDSDB_API_KEY)
mindsdb_server = MindsDBServer(config=minds_config)
minds_agent = MindsAgent(server=mindsdb_server, 
                            config=minds_config, 
                            api_key=MINDSDB_API_KEY)

max_retries = 5


if __name__ == "__main__": 

    prompt = "What is the best gift for Valentine?"
    scrape_prompt = f"Summarize the document in 3 sentences and suggest a gift based on those information {prompt}. Your answer must be in JSON formed of summary & suggest"
    search_results = tavily.run(prompt, **search_config)

    urls = [res['url'] for res in search_results['results']]
    rand_idx = random.randint(0, len(urls) - 1)
    print(urls[rand_idx])
    print("=========="*10)
    scrape_result = scraper.run(input=scrape_prompt, 
                                url=urls[rand_idx])
    if scrape_result: 
        print(scrape_result)
        print(type(scrape_result))
        print(scrape_result)
        print(scrape_result['summary'])
        print(scrape_result['suggest'])

    suggest_resource = scrape_result['summary'] + "\n" + scrape_result['suggest']
    prompt = prompt + f"Here are some additional information that can help your results:\n{suggest_resource}"
    result = minds_agent.run(input=prompt)

"""
Valentine's Day is a special occasion to express love for your romantic partner, friends, and family. The website offers a comprehensive gift guide for various loved ones. The gift suggestions go beyond cliched chocolates and flowers, focusing on thoughtful and meaningful presents.
The best gift for Valentine's Day would be a thoughtful and personalized gift that shows your loved one how much you care. Consider gifts like personalized photo albums, custom jewelry, or a spa day experience to make the day truly special.
"""