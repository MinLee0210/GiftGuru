import json
from scrapegraphai.graphs import SmartScraperGraph

from giftguru.engines.base import Node

class ScrapeWebWorker(Node): 
    def __init__(self, config, api_key=None, name="ScrapeGraphAI"): 
        super().__init__(name=name,api_key=api_key)
        self.config = config
        self.config['llm']['api_key'] = api_key
        
    def run(self, input, url:str, log=False):
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