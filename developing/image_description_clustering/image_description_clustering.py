import logging
import os
from pathlib import Path

import torch
import torch.optim as optim
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    kMeansModel = KMeans(n_clusters=number_of_clusters,
                         init='k-means++',
                         max_iter=100,
                         n_init=1)
    kMeansModel.fit(X)
    order_centroids = kMeansModel.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    cluster_file_path = data_dir / "clusters"
    for i in range(number_of_clusters):
        logger.info("Cluster %d:" % i)
        with open(cluster_file_path / f"cluster_{i}.txt", 'w') as f:
            for ind in order_centroids[i, :10]:
                logger.info(' \t%s' % terms[ind])
                f.write(terms[ind] + '\n')
    # Log the filename and its corresponding cluster
    for filename, label in zip(description_filenames, kMeansModel.labels_):
        logger.info(f"File :{filename} is in cluster {label}")

    # Load pre-trained model tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Tokenize text
    inputs = tokenizer(descriptions, padding=True, truncation=True, return_tensors="pt")
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    # Convert to tensors
    input_ids = input_ids.clone().detach()

    # Use the KMeans labels as targets for BERT
    labels = torch.tensor(kMeansModel.labels_).long()

    # Load BERT model
    bertModel = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=number_of_clusters)

    # Optimizer
    optimizer = optim.Adam(bertModel.parameters(), lr=0.001)

    # Dataloader
    data = list(zip(input_ids,  attention_mask.clone().detach(), labels.clone().detach()))
    dataloader = DataLoader(data, batch_size=32)

    # Start fine-tuning BERT
    for epoch in range(10):  # Number of epochs is an hyperparameter you can choose
        for batch in dataloader:
            logger.info(f"epoch done: {epoch}")
            b_input_ids, b_attention_mask, b_labels = batch
            outputs = bertModel(b_input_ids, attention_mask=b_attention_mask, labels=b_labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
    # Let's assume you have a new document that you want to classify
    new_doc = """The image shows a person standing on what appears to be a beach with wet sand. The individual is wearing a cap and has some sort of gear or clothing that might suggest they are involved in outdoor activities or environmental work, possibly related to marine life given the context.

In front of the person are several large objects that resemble whale carcasses, suggesting they have been beached. The beach looks relatively remote with vegetation on the horizon and a cloudy sky above. It's not clear what the purpose is for this person being there, but it could relate to monitoring, research, or response activities related to marine life or environmental conservation.
"""

    # The trained model expects the input in a certain format so
    # let's preprocess our new document accordingly
    inputs = tokenizer(new_doc, padding=True, truncation=True, return_tensors="pt")

    # Use the model to get the prediction probabilities
    bertModel.eval()  # set the model to evaluation mode
    with torch.no_grad():
        outputs = bertModel(**inputs)  # pass the new document through the model

    # The outputs are logits. The argmax of the logits would give the predicted cluster.
    predictions = torch.argmax(outputs.logits, dim=-1)

    print(f"The new document was classified as being in cluster: {predictions.item()}")
