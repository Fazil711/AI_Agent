class StateService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateService, cls).__new__(cls)
            cls.reset(cls._instance)
        return cls._instance

    def reset(self):
        """Clears all in-memory references to data."""
        self.vectordb = None
        self.dataframes = []

brain_state = StateService()