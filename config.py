class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database_file.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'
    SWAGGER_CONFIG = {
        'title': 'AutoScaler API',
        'uiversion': 3
    }

    # Auto-scaling parameters
    TARGET_CPU = 0.80
    SLEEP_INTERVAL = 10  # Adjust as needed
    MAX_REPLICAS_CHANGE = 50  # Maximum allowed change in replicas

    # Default port if not specified
    DEFAULT_PORT = 8213
