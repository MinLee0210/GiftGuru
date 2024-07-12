import mindsdb_sdk

class MindsDBServer: 
    def __init__(self, config): 
        self.config=config
        self.server = self.setup_server()
        self.project = self.setup_project()

    def setup_server(self): 
        try: 
            server = mindsdb_sdk.connect(self.config['url'])
            return server
        except Exception as e: 
            return e

    def setup_project(self): 
        try: 
            project = self.server.create_project(self.config['project'])
        except: 
            project = self.server.get_project(self.config['project'])

        return project

