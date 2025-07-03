from app import create_app
from datetime import datetime
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    app.run(debug=True) 