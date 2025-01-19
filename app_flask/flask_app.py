from flask import Flask, request
import logging
from random import randint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if 'ctest' in request.cookies:
        try:
            json_data = request.get_json()
            logger.info(f"Received JSON (Flask): {json_data}")
        except Exception as e:
            logger.error(f"Error processing JSON: {e}")
    
    # if randint(1, 25) >= 24:
    #     1 / 0
    return "OK flask", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
