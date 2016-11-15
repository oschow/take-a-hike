from flask import Flask, request, render_template
import pandas as pd
import graphlab as gl
import cPickle as pickle
import random

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

def random_five(recs):
	hike_info = []
	for rec in recs:
		info = sf_hikes[sf_hikes['hike_name']==rec]
		hike_info.append(info)
	pick_5 = random.sample(hike_info, 5)
	return pick_5

def filter_recs(hikes_sorted, miles, elevation, dog):
	recs = []
	for rec in hikes_sorted:
		if miles == "Less than 2 miles":
			if rec['total_distance'] <= 2.0:
				recs.append(rec)
		elif miles == "2 - 5 miles":
			if rec['total_distance'] > 2.0 and rec['total_distance'] <= 5.0:
				recs.append(rec)
		elif miles == "5 - 10 miles":
			if rec['total_distance'] > 5.0 and rec['total_distance'] <= 10.0:
				recs.append(rec)
		elif miles == "More than 10 miles":
			if rec['total_distance'] > 10.0:
				recs.append(rec)
		else:
			continue
	recs2 = []
	for rec in recs:
		if elevation == "Less than 500 ft":
			if rec['elevation_gain'] <= 500:
				recs2.append(rec)
		elif elevation == "500 - 1000 ft":
			if rec['elevation_gain'] > 500 and rec['elevation_gain'] <= 1000:
				recs2.append(rec)
		elif elevation == "1000 - 2000 ft":
			if rec['elevation_gain'] > 1000 and rec['elevation_gain'] <= 2000:
				recs2.append(rec)
		elif elevation == "More than 2000 ft":
			if rec['elevation_gain'] > 2000:
				recs2.append(rec)
		else:
			continue
	if recs2 == []:
		return None
	else:
		recs3 = []
		for rec in recs2:
			if dog == "Don't care":
				recs3.append(rec)
			elif dog == 'Yes':
				if rec['dog_friendly'] == 1:
					recs3.append(rec)
			elif dog == 'No':
				if rec['dog_friendly'] == 0:
					recs3.append(rec)
			else:
				continue
		if recs3 == []:
			return None
		else:
			return recs3



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
	if hike == '':
		hikes_sorted = sf_hikes.sort('stars', ascending=False)
		miles = request.form.get('num-miles')
		elevation = request.form.get('elevation-gain')
		dog = request.form.get('dog')
		recs = filter_recs(hikes_sorted, miles, elevation, dog)
		if recs == None:
			return render_template('error.html')
		else:
			my_recs = random.sample(recs, 5)
			return render_template('make-recs.html', my_recs=my_recs)
	else:
		recs = content_model.recommend_from_interactions([hike], k=5)
		your_hike = get_info(hike)
		hike_data = get_hike_info(recs)
		return render_template('make-recommendations.html', your_hike=your_hike, hike_data=hike_data)

@app.route('/popular-hikes', methods=['POST', 'GET'])
def get_popular():
	recs = []
	rec_ids = popular_model.recommend_from_interactions(['hike1'],k=20)
	for h_id in rec_ids:
		hike = h_id['hike_id']
		recs.append(hike_ids[hike])
	best_hikes = random_five(recs)
	return render_template('get-popular.html', best_hikes=best_hikes)


if __name__ == '__main__':
	sf_hikes = gl.SFrame('../data/all_hikes_with_hike_name.csv')
	sf_hikes = sf_hikes.remove_column('hike_id')
	sf_ratings = gl.SFrame('../data/all_ratings_matrix.csv')
	hike_side_data = gl.SFrame('../data/all_hikes_with_hike_id.csv')
	with open('../data/all_hike_ids.pkl') as f:
		hike_ids = pickle.load(f)

	content_model = gl.load_model('hike_content_recommender')
	popular_model = gl.load_model('hike_popularity_recommender')

	app.run(host='0.0.0.0', port=1111, debug=True)
