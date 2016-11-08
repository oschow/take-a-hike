from flask import Flask, request, render_template
import pandas as pd
import graphlab as gl

app = Flask(__name__)

def get_hike_info(recs):
	sf = gl.SFrame('../data/final.csv')
	hike_info = []
	for rec in recs:
		hike = rec['hike_name']
		info = sf[sf['hike_name']==hike]
		hike_info.append(info)
	return hike_info


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
	hike_data = get_hike_info(recs)
	return render_template('make-recommendations.html', hike_data=hike_data)


if __name__ == '__main__':
	model = gl.load_model('content_recommender')
	app.run(host='0.0.0.0', port=7070, debug=True)
