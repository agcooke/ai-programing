import os
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os

if __name__ == '__main__':
    current_file_path = Path(os.path.realpath(__file__)).parent.parent.parent
    data_dir = current_file_path / "images"
    logger.info("Loading data from %s" % data_dir)
    filenames = list(data_dir.glob('*.txt'))
    descriptions = []
    description_filenames = []  # Store filenames in the same order as descriptions
    logger.info("Total number of images: %d" % len(filenames))
    for filename in filenames:
        logger.info("Loading file %s" % filename)
        with open(filename, 'r') as f:
            descriptions.append(f.read())
            description_filenames.append(filename)
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(descriptions)
    number_of_clusters = 3
    model = KMeans(n_clusters=number_of_clusters,
                   init='k-means++',
                   max_iter=100,
                   n_init=1)
    model.fit(X)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    cluster_file_path = data_dir / "clusters"
    for i in range(number_of_clusters):
        logger.info("Cluster %d:" % i)
        with open(cluster_file_path / f"cluster_{i}.txt", 'w') as f:
            for ind in order_centroids[i, :10]:
                logger.info(' \t%s' % terms[ind])
                f.write(terms[ind] + '\n')
    # Log the filename and its corresponding cluster
    for filename, label in zip(description_filenames, model.labels_):
        logger.info(f"File :{filename} is in cluster {label}")
