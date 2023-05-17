from flask import Flask, request, jsonify
import requests
import os
import shutil

import predictor

app = Flask(__name__)
github_path_to_classifier = "https://github.com/remla23-team04/model-training/raw/main/data/trained_models/"    # Trained model
github_path_to_sentiment_model = "https://github.com/remla23-team04/model-training/raw/main/data/output/"      # .pkl files
temp_path_to_trained_models = os.path.join("temp", "trained_models")
temp_path_to_sentiment_models = os.path.join("temp", "sentiment_models")


@app.route('/')
def root():
    """
    Root endpoint of model-service.
    :return:
    """
    return "Nice, model-service is running"


@app.route('/clean', methods=['GET'])
def clean():
    """
    Cleans the temp folder and resets the directory tree.
    :return:
    """
    if os.path.exists("temp"):
        shutil.rmtree("temp")
    os.mkdir("temp")
    os.mkdir(temp_path_to_trained_models)
    os.mkdir(temp_path_to_sentiment_models)
    return "Temp folder is now empty!"


@app.route('/download/<classifier_name>/<sentiment_model_name>/<version>', methods=['GET'])
def download(classifier_name, sentiment_model_name, version):
    # print(classifier_name, version)
    classifier_filename = classifier_name + "_" + version
    classifier_temp_file_path = os.path.join(temp_path_to_trained_models, classifier_filename)

    model_filename = sentiment_model_name + "_" + version
    model_temp_file_path = os.path.join(temp_path_to_sentiment_models, model_filename) + '.pkl'
    # print(temp_file_path)
    if os.path.isfile(classifier_temp_file_path) and os.path.isfile(model_temp_file_path):
        return "File exists, don't download again!"

    classifier_req = requests.get(github_path_to_classifier + classifier_filename)
    model_req = requests.get(github_path_to_sentiment_model + model_filename + '.pkl')
    print("Downloading from: " + str(github_path_to_sentiment_model + model_filename + '.pkl'))
    if classifier_req.ok and model_req.ok:
        # Download classifier
        if classifier_req.ok:
            f = open(classifier_temp_file_path, 'wb')
            f.write(classifier_req.content)

        # Download sentiment model
        if model_req.ok:
            f = open(model_temp_file_path, 'wb')
            f.write(model_req.content)

        return "Downloaded files!"

    return "Failed to download: " + github_path_to_classifier + classifier_filename \
           + "<br> It's probably because there is no trained model with this name: " \
           + classifier_filename + ", version: " + version + \
           "<br> OR <br> Failed to download: " + github_path_to_sentiment_model + model_filename + '.pkl' \
           + "<br> It's probably because there is no trained model with this name: " \
           + model_filename + ", version: " + version


# curl -X POST -H "Content-Type:application/json" -d "\"This is my review\"" "localhost:5000/predict"
# curl -X POST -H "Content-Type:application/json" -d "\"This is my good review\"" "localhost:5000/predict"
@app.route('/predict',methods = ['POST'])
def predict():
   review_string = request.json['review']
   app.logger.warning(f"predicting for review: {review_string}")
   sentiment = get_sentiment(review_string)
   app.logger.warning(f"response sentiment: {sentiment}")
   return jsonify(sentiment=sentiment)


def get_sentiment(review):
    ## TAKES LATEST VERSION, TODO: maybe allow the user to pick version of the model???
    version = min(len(os.listdir(temp_path_to_trained_models)), len(os.listdir(temp_path_to_sentiment_models))) - 1
    print(version)
    if version == -1:
        return "There is no model downloaded!"

    sentiment_model_name = "c1_BoW_Sentiment_Model_0.pkl" # TODO: Hardcoded now but might wanna allow the use to select this via the request
    bow_dictionary_path = os.path.join(temp_path_to_sentiment_models, sentiment_model_name)
    classifier_name = "c2_Classifier_Sentiment_Model_0" # TODO: Hardcoded now but might wanna allow the use to select there via the request
    classifier_path = os.path.join(temp_path_to_trained_models, classifier_name)
    prediction = predictor.predict(bow_dictionary_path, classifier_path, review)
    return prediction



if __name__ == '__main__':
    # Clear downloaded models and set up directory tree
    clean()
    # Download at least one model
    download("c2_Classifier_Sentiment_Model", "c1_BoW_Sentiment_Model", "0")
    # host 0.0.0.0 to listen to all ip's
    app.run(host='0.0.0.0', port = 5001)
