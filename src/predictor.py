import os
import pickle
import joblib

def predict(bow_dictionary_path, classifier_path, review):
    # Loading BoW dictionary
    print(os.path.isfile(bow_dictionary_path))
    print(classifier_path)
    cv = pickle.load(open(bow_dictionary_path, "rb"))

    #### PREDICTION
    classifier = joblib.load(classifier_path)

    processed_input = cv.transform([review]).toarray()[0]
    prediction = classifier.predict([processed_input])[0]
    prediction_map = {
        0: "negative",
        1: "positive"
    }
    print("The model believes the review \"" + review + f"\" is {prediction_map[prediction]}.")
    return prediction_map[prediction]
