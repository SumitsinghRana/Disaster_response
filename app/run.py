import json
import plotly
import pandas as pd

from utils.translator import detect_and_translate
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from utils.urgency import get_urgency, extract_locations
from utils.translator import detect_and_translate
from utils.map_utils import generate_map

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse_table', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    category_names = df.iloc[:, 4:].columns
    category_counts = (df.iloc[:, 4:]!=0).sum()
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        
        {
            'data': [
                Bar(
                    x=category_names,
                    y=category_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Categories',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        }
        
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


@app.route('/map')
def show_map():
    return render_template('map.html')
# web page that handles user query and displays model results
@app.route('/go')
def go():
    query = request.args.get('query', '')

    # translation
    translated_query, original_lang = detect_and_translate(query)

    # ML prediction
    classification_labels = model.predict([translated_query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # urgency
    urgency_level, urgency_style = get_urgency(translated_query)

    # location extraction
    locations = extract_locations(translated_query)

    # generate map
    generate_map(locations, urgency_style)

    return render_template(
        'go.html',
        query=query,
        original_lang=original_lang,
        translated_query=translated_query,
        classification_results=classification_results,
        urgency_level=urgency_level,
        urgency_style=urgency_style,
        locations=locations
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()