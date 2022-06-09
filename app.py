import util_scrap

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app_port = 80
CORS(app)


@app.post("/getArticle")
def get_article():
    return jsonify(util_scrap.get_article(request.json["link"]))


@app.get("/getListArticleByCategory/<category>/<page>")
def get_list_article_by_category(category, page):
    return jsonify(util_scrap.get_list_article_by_category(category, page))


@app.get("/getListArticleByKeyword/<keyword>")
def get_list_article_by_keyword(keyword):
    return jsonify(util_scrap.get_list_article_by_keyword(keyword))


if __name__ == '__main__':
    app.run(debug=False, port=app_port)