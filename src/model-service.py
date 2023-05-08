from flask import Flask, request, jsonify
import requests
import os
import shutil

app = Flask(__name__)
github_path_to_trained_models = "https://github.com/remla23-team04/model-training/raw/main/data/trained_models/"
temp_path_to_trained_models = os.path.join("temp", "trained_models")


@app.route('/')
def root():
    """
    Root endpoint of model-service.
    :return:
    """
    return "Nice, model-service is running"


@app.route('/clean')
def clean():
    """
    Cleans the temp folder and resets the directory tree.
    :return:
    """
    shutil.rmtree("temp")
    os.mkdir("temp")
    os.mkdir(temp_path_to_trained_models)
    return "Temp folder is now empty!"


@app.route('/download/<name>/<version>')
def download(name, version):
    print(name, version)
    filename = name + "_" + version
    temp_file_path = os.path.join(temp_path_to_trained_models, filename)
    print(temp_file_path)
    if os.path.isfile(temp_file_path):
        return "File exists, don't download again!"

    r = requests.get(github_path_to_trained_models + filename)
    if r.ok:
        f = open(temp_file_path, 'wb')
        f.write(r.content)
        return "Downloaded: " + github_path_to_trained_models + filename

    return "Failed to download: " + github_path_to_trained_models + filename \
           + "<br> It's probably because there is no trained model with this name / version: " + filename


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
    if "good" in review:
        return "positive"
    else:
        return "negative"



if __name__ == '__main__':
    # host 0.0.0.0 to listen to all ip's
    app.run(host='0.0.0.0')
