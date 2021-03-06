#our classifier
import ml.classifier as clf
from fastapi import FastAPI, Body
from joblib import load
from prometheus_fastapi_instrumentator import Instrumentator
from mangum import Mangum

#Iris data structure
from schema.iris import Iris

#define the fastapi
app = FastAPI(title="Iris Prediction API",
              description="API for Iris Prediction",
              version="1.0")

handler = Mangum(app)

#when the app start, load the model
@app.on_event('startup')
async def load_model():
    clf.model = load('ml/iris_v1.joblib')
    
#when post event happens to /predict
@app.post('/predict')
async def get_prediction(iris:Iris):
    data = dict(iris)['data']
    prediction = clf.model.predict(data).tolist()
    proba = clf.model.predict_proba(data).tolist() 
    return  {"prediction": prediction,
            "probability": proba}

@app.get("/")
async def root():
    return {"message": "Yay! Change?"}

Instrumentator().instrument(app).expose(app)
    


