from flask import Flask, request, render_template
import pandas as pd
import graphlab as gl

app = Flask(__name__)

def clean_df(df):
	df['area_of_co'] = df['area_of_co'].map({'Aspen-Snowmass': 'Aspen/Snowmass', 'boulder-denver-golden-fort-collins-lyons': 'Denver/Boulder/Golden', 'colorado-national-monument': 'CO National Monument', 'great-sand-dunes-national-park': 'Great Sand Dunes National Park', 'indian-peaks-wilderness-area-james-peak-wilderness-area': 'Indian Peaks/James Peak Wilderness Area', 'rocky-mountain-national-park': 'Rocky Mountain National Park', 'summit-county-eagle-county-clear-creek-county': 'Summit/Eagle/Clear Creek County'})
	df['drive_time_from_denver'] = df['drive_time_from_denver'].map(lambda x: ("%.2f" % x))
	df['hike_url'] = df['hike_url'].apply(lambda x: x.strip())
	return df

def list_hikes(sf):
	hikes = []
	for h in sf['hike_name']:
		hikes.append(h)
	return hikes

def list_regions(sf):
	regions = sf['area_of_co'].unique()
	return regions

def get_hike_info(recs):
	hike_info = []
	for rec in recs:
		hike = rec['hike_name']
		info = sf[sf['hike_name']==hike]
		hike_info.append(info)
	return hike_info


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/choose-hike', methods=['GET', 'POST'])
def enter_hike():
	hikes = list_hikes(sf)
	regions = list_regions(sf)
	return render_template('choose-hike.html', hikes=hikes, regions=regions)


@app.route('/make-recommendations', methods=['POST', 'GET'])
def get_recommendations():
	hike = request.form.get('hike-name')
	region = request.form.get('region-name')
	miles = request.form.get('miles')
	elevation = request.form.get('elevation')
	# if region != None:
	# 	sf_new = sf[sf['area_of_co']== region]
	# 	model = gl.recommender.item_content_recommender.create(sf_new, item_id='hike_name')
	recs = model.recommend_from_interactions([hike], k=5)
	hike_data = get_hike_info(recs)
	return render_template('make-recommendations.html', hike_data=hike_data)


if __name__ == '__main__':
	df = pd.read_csv('../data/final_with_url.csv')
	df = clean_df(df)
	sf = gl.SFrame(df)
	model = gl.load_model('content_recommender')
	app.run(host='0.0.0.0', port=7070, debug=True)
