import os
import requests
from flask import Flask, Response
from bs4 import BeautifulSoup
import pysnooper

app = Flask(__name__)


def get_simile():
    response = requests.get("https://random-simile-generator.herokuapp.com/")

    soup = BeautifulSoup(response.content, "html.parser")
    simile = soup.find_all("div", id="content")
    simile = simile[0].getText()
    return simile.strip()

# @pysnooper.snoop(depth=2)
def pig_latinize():
    simile = get_simile().strip("\"")
    form_data = {'input_text': simile}
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/", data=form_data, allow_redirects=False)
    link = response.headers['Location']

    return link


@app.route('/')
def home():
    piglatin_simile = pig_latinize()
    simile = get_simile()
    return f"<a href={piglatin_simile}>Click here to see pig latin-ized simile</a>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
