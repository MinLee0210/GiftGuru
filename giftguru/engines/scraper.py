import random
from scrapegraphai.graphs import SmartScraperGraph

from giftguru.engines.base import Node

class ScrapeWebWorker(Node): 
    def __init__(self, config, api_key=None, name="ScrapeGraphAI"): 
        super().__init__(name=name,api_key=api_key)
        self.config = config
        self.config['llm']['api_key'] = api_key
        
    def run(self, input, url:str, max_retries=3):
        while max_retries > 0: 
            scrape_result  = self.call_llm(input, url)
            if scrape_result: 
                break
            max_retries -= 1
            scrape_result = "None"
        return scrape_result

        
    def call_llm(self, input, url): 
        try: 
            smart_scraper_graph = SmartScraperGraph(
                                                    prompt=input,
                                                    source=url,
                                                    config=self.config
                                                    )
            result = smart_scraper_graph.run()
            return result
        except: 
            return None