import pandas as pd
import graphlab as gl

def create_content_recommender(sf_hikes):
    model = gl.recommender.item_content_recommender.create(sf_hikes, item_id='hike_name')
    model.save('web_app/hike_content_recommender')

def create_popularity_recommender(sf_ratings, hike_side_data):
    model = gl.recommender.popularity_recommender.create(sf_ratings, user_id='variable', item_id='hike_id', target='value', item_data=hike_side_data)
    model.save('web_app/hike_popularity_recommender')

if __name__ == '__main__':
    sf_hikes = gl.SFrame('data/hikes_data_with_hike_name.csv')
    sf_hikes = sf_hikes.remove_column('hike_id')
    sf_ratings = gl.SFrame('data/ratings_matrix.csv')
    hike_side_data = gl.SFrame('data/hikes_data_with_hike_id.csv')

    create_content_recommender(sf_hikes)
    create_popularity_recommender(sf_ratings, hike_side_data)
