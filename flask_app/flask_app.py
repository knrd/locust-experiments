from flask import Flask, request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    if 'ctest' in request.cookies:
        try:
            json_data = request.get_json()
            logger.info(f"Received JSON (Flask): {json_data}")
        except Exception as e:
            logger.error(f"Error processing JSON: {e}")
    
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)
