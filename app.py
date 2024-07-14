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

from utils import yaml_read, load_image

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
    st.image(load_image(image_str="./static/giftguru_logo.jpeg"))
    st.header("Input")
    prompt = st.text_area("Best gift is the best to give!", placeholder="Let's us know")

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

    st.divider()
    st.markdown("""
## 📍 Overview

GiftGuru is your AI-powered gift-giving companion, here to help you find the perfect present for any occasion. Whether it's Valentine's Day, Christmas, a birthday, or just because, our intelligent system uses cutting-edge AI to suggest thoughtful and personalized gift ideas tailored to your recipient's unique tastes and preferences.

## 🤖 Technologies Used

* **MindsDB:** Our intelligent gift-giving agent is built on MindsDB, a powerful AI engine that enables us to understand complex relationships and generate insightful recommendations.
* **Tavily:** We leverage Tavily's expertise in personalized recommendations to ensure our suggestions are truly relevant and engaging.
* **ScrapeGraphAI:** Our data scraping engine, powered by ScrapeGraphAI, keeps us up-to-date on the latest trends, reviews, and pricing information across a vast range of products and services.


## 🧩 Features

* **Personalized Recommendations:** GiftGuru takes into account your recipient's interests, hobbies, age, relationship to you, and even past gift preferences to suggest truly meaningful and unique gifts.
* **Occasion-Specific Suggestions:**  Need a Valentine's Day gift for your significant other, a birthday present for your best friend, or a thoughtful stocking stuffer for your niece? GiftGuru has you covered with tailored suggestions for every occasion.
* **Creative & Unique Ideas:**  Go beyond the ordinary with our AI-powered suggestions. We uncover hidden gems and unique gifts you might not find anywhere else.
* **Easy-to-Use Interface:**  Finding the perfect gift has never been easier. Our intuitive interface makes navigating through suggestions and exploring options a breeze.
                """)
    st.markdown("""
## 🎯 Workflow
GiftGuru employs a multi-faceted approach to guide users towards thoughtful and meaningful
gifts. Our methodology leverages a combination of cutting-edge technologies and human-centric
insights, ensuring a personalized and enriching gift-giving experience.
""")
    st.image(load_image(image_str="./static/workflow.png"))
    st.markdown("""
The process is as follows:

1. **Understanding Your Needs**: GiftGuru starts by capturing the essence of your gift-giving
intention. Through a simple, user-friendly interface, you'll provide details about the
recipient, their interests, and the occasion.

2. **The Knowledge Graph**: This is where our "brain" comes into play. GiftGuru utilizes a
sophisticated knowledge graph, built from vast amounts of curated data about products,
people, and relationships. This graph allows us to understand the intricate connections
between different gift ideas and recipient preferences.

3. The Search and Selection Process:

  + *TavilySearchAPI*: We leverage a powerful search engine API to uncover relevant
product information from a vast online marketplace. This ensures a
comprehensive range of gift options.
  + *ScrapeGraphAI*: To enhance the accuracy and relevance of our suggestions, we
employ a specialized AI that analyzes product reviews, popularity trends, and user
feedback. This helps identify truly meaningful gifts that align with the recipient's
preferences.

4. **Personalized Recommendations**: Drawing upon the knowledge graph, search results, and
AI-powered analysis, GiftGuru generates a personalized recommendation and several
websites that user’s can refer to to improve their choices of gifts
                """)
    
    st.markdown("👾 Gallery")
    st.image(load_image("./static/gg_example.png"))
    st.markdown("""
## 🧑‍💻 Contact

+ **Gmail**: minh.leduc.0210@gmail.com
+ **LinkedIn**: https://www.linkedin.com/in/minh-le-duc-a62863172/
+ **Medium**: https://medium.com/@octoopt_8888
                """)