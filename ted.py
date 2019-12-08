from flask import Flask, render_template, url_for, request
from ted_engine import ted_engine
import pdb
import trace

pdb.set_trace()
app = Flask(__name__)
ted = ted_engine()
result = []


@app.route("/")
def home():
    return render_template('index.html', data=ted.tedData, result=result, search=False)


@app.route("/", methods=['POST'])
def process():
    # Perform search
    search = request.form.get('search')
    if search is not None:
        result = ted.search(search)
        documents = []
        embed_url = []

        if len(result) < 6:
            length = len(result)
        else:
            length = 6
        for i in range(length):
            documents.append(result[i])

        title = list(ted.tedData['title'][documents])
        url = list(ted.tedData['url'][documents])
        description = list(ted.tedData['description'][documents])
        author = list(ted.tedData['main_speaker'][documents])
        categories = list(ted.tedData['ratings'][documents])

        for link in url:
            embed_url.append(link.replace("www", "embed", 1))

        return render_template('index.html', data=ted.tedData, result=documents, scroll='found', title=title,
                               url=embed_url, description=description, author=author, categories=categories,
                               search=True)

    classify = request.form.get('classify')
    categories = []
    percentage = []
    if classify is not None:
        classification = ted.classify(classify)
        for c in classification:
            categories.append(c)
            percentage.append(round(classification[c] * 100, 2))
        return render_template('index.html', scroll='classification', categories=categories,
                               percentage=percentage, classification=classification, search=False)

    recommend = request.form.get('docID')
    if recommend is not None:
        recommendID = int(recommend)
        title = ted.tedData['title'][recommendID]
        description = ted.tedData['description'][recommendID]
        author = ted.tedData['main_speaker'][recommendID]
        categories = ted.tedData['ratings'][recommendID]

        context = title + " " + description + " " + author + " " + categories

        result = ted.recommend(recommendID, context)
        documents = []
        embed_url = []

        if len(result) < 6:
            length = len(result)
        else:
            length = 6
        for i in range(length):
            documents.append(result[i])

        title = list(ted.tedData['title'][documents])
        url = list(ted.tedData['url'][documents])
        description = list(ted.tedData['description'][documents])
        author = list(ted.tedData['main_speaker'][documents])
        categories = list(ted.tedData['ratings'][documents])

        for link in url:
            embed_url.append(link.replace("www", "embed", 1))

        return render_template('index.html', data=ted.tedData,
                               result=documents, scroll='found', title=title, url=embed_url,
                               description=description, author=author, categories=categories, search=True)


# if __name__ == '__main__':
    # app.run(port=5000, debug=False)
# app.run(host="0.0.0.0", port="80", debug=False)
