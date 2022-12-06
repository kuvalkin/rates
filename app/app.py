from flask import Flask

from controllers import rates

app = Flask(__name__)


@app.get("/rates")
def rates_endpoint():
    return rates.get()
