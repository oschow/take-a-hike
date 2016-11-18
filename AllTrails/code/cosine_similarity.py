import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity

def cos_sim_recommendations(hike_idx, df, index_name, n=5):
    hike = df.iloc[hike_idx]
    cs = cosine_similarity(hike, df)
    # cs = cosine_similarity(X, y).mean(axis=1)
    rec_index = np.argsort(cs)[0][-6:][::-1][1:]
    recommendations = []
    for rec in rec_index:
        recommendations.append(index_name[rec])
    return recommendations


if __name__ == '__main__':
    df = pd.read_csv('data/hikes_data_with_hike_name.csv')
    index_name = df['hike_name'].values
    df.drop('hike_name', axis=1, inplace=True)
    df.drop('hike_region', axis=1, inplace=True)
    df.drop('hike_id', axis=1, inplace=True)

    hike_name = 'Maxwell Falls Lower Trail'
    for idx, name in enumerate(index_name):
        if name == hike_name:
            hike_idx = idx
    recommendations = cos_sim_recommendations(hike_idx, df, index_name, n=5)
