import os 
import nest_asyncio
import random

from dotenv import load_dotenv

from giftguru.engines.scraper import ScrapeWebWorker
from giftguru.engines.search import TavilyWorker

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

tavily = TavilyWorker(api_key=TAVILY_API_KEY)
scraper = ScrapeWebWorker(config=scraper_config, 
                          api_key=MINDSDB_API_KEY)

if __name__ == "__main__": 
    max_retries = 5
    prompt = "What is the best gift for Valentine?"
    scrape_prompt = f"Summarize the document in 3 sentences and suggest a gift based on those information {prompt}. Your answer must be in formed of summary & suggest"
    search_results = tavily.run(prompt, **search_config)
    # print(search_results)
    print("=========="*10)
    while max_retries > 0: 
        urls = [res['url'] for res in search_results['results']]
        rand_idx = random.randint(0, len(urls) - 1)
        print(urls[rand_idx])
        print("=========="*10)
        scrape_result = scraper.run(input=scrape_prompt, 
                                    url=urls[rand_idx])
        if scrape_result: 
            print(scrape_result)
            print(type(scrape_result))
            print(scrape_result['summary'])
            print(scrape_result['suggest'])
            break
        print("Retry scraping")
        max_retries -= 1