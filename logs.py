from flask import Flask
from ksp.logger import logging

logging.info("starting app")

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    logging.info("testing logging file")
    return "welcome to app"

if __name__ == '__main__':
    app.run(debug=True)