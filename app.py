# Calling necessary libraries
import os 
import nest_asyncio
import random

from dotenv import load_dotenv

import streamlit as st

from giftguru.engines.scraper import ScrapeWebWorker
from giftguru.engines.search import TavilyWorker
from giftguru.mindsdb.server import MindsDBServer
from giftguru.mindsdb.agent import MindsAgent
from giftguru.prompts import SCRAPER_PROMPT, MINDS_AGENT_SUFFIX

from utils import yaml_read

load_dotenv()
nest_asyncio.apply()


# Setting up variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MINDSDB_API_KEY = os.getenv("MINDSDB_API_KEY")

config = yaml_read(dir='./config.yaml')
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

if __name__ == "__main__": 

    st.title("GiftGuru")
    st.subheader("Make your gifts more meaningful!")

    st.header("Input")
    prompt = st.text_input("Best gift is the best to give!", placeholder="Let's us know")

    if prompt: 
        with st.status("Please wait ..."):
            # Searching and Scraping
            scrape_prompt = SCRAPER_PROMPT.format(prompt=prompt)
            print(scrape_prompt)
            search_results = tavily.run(prompt, **search_config)
            urls = [res['url'] for res in search_results['results']]
            rand_idx = random.randint(0, len(urls) - 1)
            scrape_result = scraper.run(input=scrape_prompt, 
                                        url=urls[rand_idx])
            print(scrape_result)
            # MindsDB agent
            suggest_resource = scrape_result['summary'] + "\n" + scrape_result['suggest']
            print(suggest_resource)
            mindsdb_prompt = MINDS_AGENT_SUFFIX.format(suggest_resource=suggest_resource)
            result = minds_agent.run(input=prompt)

            st.subheader("Your best crafts are ...")
            st.write(result)

            st.subheader("Here are some websites that you can visit: ")
            for url in urls: 
                st.markdown("-" + url)

    st.header("Document")