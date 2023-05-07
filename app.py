from flask import Flask
from flask import request
import requests
import os
import shutil

app = Flask(__name__)
github_path_to_classifier = "https://github.com/remla23-team04/model-training/raw/main/data/trained_models/"    # Trained model
github_path_to_sentiment_model = "https://github.com/remla23-team04/model-training/blob/main/data/output/"      # .pkl files
temp_path_to_trained_models = os.path.join("temp", "trained_models")
temp_path_to_sentiment_models = os.path.join("temp", "sentiment_models")


@app.route('/clean', methods=['GET'])
def clean():
    """
    Cleans the temp folder and resets the directory tree.
    :return:
    """
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


@app.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.get_json()
    print(data)

    return data

if __name__ == '__main__':
    app.run()
