
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn import metrics
from time import time
import numpy as np
import generate_model as gm

def silho():
    svd = TruncatedSVD(gm.kmeans.n_clusters)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    X = lsa.fit_transform(gm.X3)

    explained_variance = svd.explained_variance_ratio_.sum()

    return metrics.silhouette_score(X, gm.kmeans.labels_, sample_size=1000)

print("Silhouette Score: ", silho())
