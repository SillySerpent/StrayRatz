from app import create_app
from datetime import datetime
from config import DevelopmentConfig, Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = create_app(Config)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug, port=port) 