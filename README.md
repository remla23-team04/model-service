# model-service

Using Python 3.8 and Conda.

Run app.py and see responses at: http://127.0.0.1:5000

### Endpoints
| Endpoint                                                     | Description                                                          | Example                                                                               |
|--------------------------------------------------------------|----------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `clean`                                                      | Removes everything from temp folder and sets up the folder structure | http://127.0.0.1:5000/clean                                                           |
| `download/<classifier_name>/<sentiment_model_name>/<version>` | Gets trained model from the `model-training` repo                    | http://127.0.0.1:5000/download/c2_Classifier_Sentiment_Model/c1_BoW_Sentiment_Model/0 |
| `submit_review`                                            | Predicts if a review is positive or negative.                        | See [postman requests](./postman_requests/REMLA.postman_collection.json)                                                      |