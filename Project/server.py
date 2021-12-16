from flask import Flask, render_template, request
from Project.cornlevel import calculate_corn_level

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', query="")

@app.route('/search')
def search():
    query = request.args.get('q')
    try:
        corn_likely_dict = calculate_corn_level(query.lower())
        return render_template('products.html', dict=corn_likely_dict)
    except:
        return render_template('index.html', query="no product found.")


if __name__ == '__main__':
  app.run(debug=True)