class StateService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateService, cls).__new__(cls)
            # Global state for the current session
            cls._instance.vectordb = None
            cls._instance.dataframes = []
        return cls._instance

# Shared instance across the application
brain_state = StateService()