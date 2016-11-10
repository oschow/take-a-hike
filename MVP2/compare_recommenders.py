import graphlab as gl
import pandas as pd

def train_model(recommenders, sf_train, item_data=None):
    model = rec.create(sf_train, user_id='variable', item_id='hike_id', target='value', item_data=item_data)
    return model

def calculate_rmse(model, sf_test):
    train_rmse = model['training_rmse']
    test_rmse = gl.evaluation.rmse(targets=sf_test['value'], predictions=model.predict(sf_test))
    return train_rmse, test_rmse


if __name__ == '__main__':
    sf = gl.SFrame('data/ratings_matrix.csv')
    sf_train, sf_test = gl.recommender.util.random_split_by_user(sf, user_id='variable', item_id='hike_id')
    hike_side_data = gl.SFrame('data/hikes_data.csv')

    recommenders = [gl.recommender,
                    gl.recommender.factorization_recommender,
                    gl.recommender.ranking_factorization_recommender,
                    gl.recommender.popularity_recommender,
                    gl.recommender.item_similarity_recommender]

    rec_names = ['Basic Recommender', 'Basic Recommender with Hike Data', 'Factorization Recommender', 'Factorization Recommender with Hike Data','Ranking Factorization Recommender', 'Ranking Factorization Recommender with Hike Data', 'Popularity Recommender', 'Popularity Recommender with Hike Data', 'Item Similarity Recommender', 'Item Similarity Recommender with Hike Data']

    trained_models = []
    for rec in recommenders:
        model = train_model(rec, sf_train)
        trained_models.append(model)
        model = train_model(rec, sf_train, item_data=hike_side_data)
        trained_models.append(model)

    for idx, mod in enumerate(trained_models):
        train_rmse, test_rmse = calculate_rmse(mod, sf_test)
        print ''
        print rec_names[idx]
        print 'Training RMSE: ', train_rmse
        print 'Test RMSE: ', test_rmse
        print ''
