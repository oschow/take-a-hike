from flask import Flask, request, render_template
import graphlab as gl
import pandas as pd
import cPickle as pickle

app = Flask(__name__)
PORT = 8080

@app.route('/')
def root():
    pass

@app.route('/user', methods=['GET', 'POST'])
def choose_hike():
	pass

@app.route('/my-recommendations', methods=['POST', 'GET'])
def get_recs():
	pass


if __name__ == '__main__':
    df = pd.read_csv('data/final')

    rec_model = gl.load_model('recommender.pkl')

    with open('something_pickled.pkl') as f:
    	something = pickle.load(f)

    app.run(host='0.0.0.0', port=PORT, debug=True)
