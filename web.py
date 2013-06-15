import requests
from django.utils.encoding import smart_str
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def wiki_fetch():
    url = (
        'http://en.wikipedia.org/w/api.php?action=query&prop=extracts&'
        'exintro=1&titles={title}&format=json&explaintext=1'
        '&exsectionformat=plain&redirects'.format(
            title=request.args.get("title", "lol")))

    response = {}
    req = requests.get(url)
    if  req.status_code == 200:
        try:
            res = req.json()["query"]["pages"]
            page_id, page = res.popitem()
            response["title"] = smart_str(
                page["title"],
                encoding="ascii",
                errors="ignore")
            response["summary"] = smart_str(
                page["extract"],
                encoding="ascii",
                errors="ignore")
        except KeyError, e:
            raise e

        return jsonify(**response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
