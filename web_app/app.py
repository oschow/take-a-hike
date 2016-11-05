from flask import Flask, request, render_template
import pandas as pd
import graphlab as gl

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html', recs=None)


@app.route('/choose-hike', methods=['GET', 'POST'])
def enter_hike():
	return render_template('choose-hike.html', recs=None)


@app.route('/make-recommendations', methods=['POST', 'GET'])
def get_recommendations():
	hike = str(request.form.get('user_input'))
	recs = model.recommend_from_interactions([hike], k=5)
	return render_template('make-recommendations.html', recs=recs)


if __name__ == '__main__':
	model = gl.load_model('content_recommender')
	app.run(host='0.0.0.0', port=6969, debug=True)
