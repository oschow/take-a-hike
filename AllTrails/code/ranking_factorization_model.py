import graphlab as gl
import pandas as pd
import cPickle as pickle

if __name__ == '__main__':
    sf = gl.SFrame('data/all_ratings_matrix.csv')
    hike_side_data = gl.SFrame('data/all_hikes_with_hike_name.csv')
    with open('data/all_hike_ids.pkl') as f:
        hike_ids = pickle.load(f)

    model = gl.recommender.ranking_factorization_recommender.create(sf, user_id='variable', item_id='hike_id', target='value', item_data=hike_side_data, ranking_regularization=0, regularization=1e-10, linear_regularization=1e-8)

    recs = model.get_similar_items(items=['hike25'], k=5)

    similar_hikes = []
    for rec in recs:
        hike = rec['similar']
        name = hike_ids[hike]
        similar_hikes.append(name)
