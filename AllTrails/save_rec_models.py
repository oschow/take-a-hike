import pandas as pd
import graphlab as gl

def create_rank_fact_recommender(sf_ratings, sf_hikes):
    model = gl.recommender.ranking_factorization_recommender.create(sf_ratings, user_id='variable', item_id='hike_id', target='value', item_data=sf_hikes, ranking_regularization=0, regularization=1e-10, linear_regularization=1e-8)
    model.save('web_app/rank_factorization_recommender')

def create_content_recommender(sf_hikes):
    sf_hikes = sf_hikes.remove_column('hike_id')
    model = gl.recommender.item_content_recommender.create(sf_hikes, item_id='hike_name')
    model.save('web_app/hike_content_recommender')

def create_popularity_recommender(sf_ratings, hike_side_data):
    model = gl.recommender.popularity_recommender.create(sf_ratings, user_id='variable', item_id='hike_id', target='value', item_data=hike_side_data)
    model.save('web_app/hike_popularity_recommender')


if __name__ == '__main__':
    sf_hikes = gl.SFrame('data/all_hikes_with_hike_name.csv')
    sf_ratings = gl.SFrame('data/all_ratings_matrix.csv')
    hike_side_data = gl.SFrame('data/all_hikes_with_hike_id.csv')

    create_rank_fact_recommender(sf_ratings, sf_hikes)
    create_content_recommender(sf_hikes)
    create_popularity_recommender(sf_ratings, hike_side_data)
