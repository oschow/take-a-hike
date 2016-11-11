from flask import Flask, request, render_template
import pandas as pd
import graphlab as gl

app = Flask(__name__)

def list_hikes(sf_hikes):
	hikes = []
	for h in sf_hikes['hike_name']:
		hikes.append(h)
	return hikes

def list_regions(sf_hikes):
	regions = sf_hikes['hike_region'].unique()
	return regions

def get_info(hike):
	data = sf_hikes[sf_hikes['hike_name']==hike]
	return data

def get_hike_info(recs):
	hike_info = []
	for rec in recs:
		hike = rec['hike_name']
		info = sf_hikes[sf_hikes['hike_name']==hike]
		hike_info.append(info)
	return hike_info


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/choose-hike', methods=['GET', 'POST'])
def enter_hike():
	hikes = list_hikes(sf_hikes)
	regions = list_regions(sf_hikes)
	return render_template('choose-hike.html', hikes=hikes, regions=regions)


@app.route('/make-recommendations', methods=['POST', 'GET'])
def get_recommendations():
	hike = request.form.get('hike-name')
	region = request.form.get('region-name')
	miles = request.form.get('num-miles')
	elevation = request.form.get('elevation-gain')
	dog = request.form.get('dog')
	recs = content_model.recommend_from_interactions([hike], k=5)
	your_hike = get_info(hike)
	hike_data = get_hike_info(recs)
	return render_template('make-recommendations.html', your_hike=your_hike, hike_data=hike_data)

@app.route('/popular-hikes', methods=['POST', 'GET'])
def get_popular():
	recs = sf_hikes[sf_hikes['stars']==5.0]
	best_hikes = get_hike_info(recs)
	return render_template('get-popular.html', best_hikes=best_hikes)


if __name__ == '__main__':
	sf_hikes = gl.SFrame('../data/hikes_data_with_hike_name.csv')
	sf_hikes = sf_hikes.remove_column('hike_id')
	sf_ratings = gl.SFrame('../data/ratings_matrix.csv')
	hike_side_data = gl.SFrame('../data/hikes_data_with_hike_id.csv')

	content_model = gl.load_model('hike_content_recommender')
	popular_model = gl.load_model('hike_popularity_recommender')

	app.run(host='0.0.0.0', port=1515, debug=True)
