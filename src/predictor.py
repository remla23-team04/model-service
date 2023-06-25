import os
import pickle
import joblib

import re                           # re = Secret Labs' Regular Expression Engine
import nltk                         # NLTK = Natural Language Toolkit

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')


def process_a_review(review):
    """
    Processing a review (should be the same as the processing of the prediction endpoint from model-training).
    :param review: the actual content - input
    :return: the processed review
    """
    # Substitute anything that is not a-zA-Z with a space
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    return ' '.join(review)


def predict(bow_dictionary_path, classifier_path, review):
    # Loading BoW dictionary
    print(os.path.isfile(bow_dictionary_path))
    print(classifier_path)
    cv = pickle.load(open(bow_dictionary_path, "rb"))

    #### PREDICTION
    classifier = joblib.load(classifier_path)

    review = process_a_review(review)

    processed_input = cv.transform([review]).toarray()[0]
    prediction = classifier.predict([processed_input])[0]
    prediction_map = {
        0: "negative",
        1: "positive"
    }
    print("The model believes the review \"" + review + f"\" is {prediction_map[prediction]}.")
    return prediction_map[prediction]
