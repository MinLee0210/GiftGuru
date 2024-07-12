class MindsAgent: 
    def __init__(self, server, config, api_key): 
        self.project = server.project
        self.server = server.server
        print(self.server.list_projects())
        self.config = config
        self.is_engine = self.__setup_engine(api_key)
        self.model = self.__setup_model()

    def __setup_engine(self, api_key): 
        try: 
            self.server.ml_engines.create(
                name=self.config['engine'],  
                handler=self.config['handler'], 
                connection_data={
                    "minds_endpoint_api_key": api_key
                }
            )
            return True
        except: 
            engine = self.server.ml_engines.list()
            print(engine)
            return False
            
    def __setup_model(self): 
        try: 
            model = self.project.models.create(name=self.config['agent_name'],
                                               predict='completion',
                                                engine=self.config['engine'],
                                                prompt_template= "You are a helpful AI assistant. Your task is to answer this {{question}}", 
                                                model_name=self.config['model_name'],
                                                )
        except: 
            model = self.project.models.get(name=self.config['agent_name'])
        return model
    
    def run(self, input, prettify=True): 
        try: 
            result = self.model.predict({"question": input})
            if prettify: 
                result = result.completion.iloc[-1]
            return result
        except: 
            return None
