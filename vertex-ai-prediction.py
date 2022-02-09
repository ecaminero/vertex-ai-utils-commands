
import os
import base64
from io import BytesIO

import cv2
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from dotenv import load_dotenv

# Load Environment
load_dotenv()
PROJECT_ID = os.environ['PROJECT_ID']
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
REGION = os.environ['PROJECT_REGION']
ENDPOINT_ID = os.environ['ENDPOINT_ID']

def encode_image(img):
    _, img_ary = cv2.imencode('*.jpg', img)
    img_bytes = img_ary.tobytes()
    buffer = BytesIO(img_bytes)
    imgb64 = base64.b64encode(buffer.getvalue()).decode()
    return imgb64
 
 
def make_prediction(imgpath, params, project_name, endpoint_region, endpoint_id):
    # The AI Platform services require regional API endpoints
    endpoint_url = f"{endpoint_region}-aiplatform.googleapis.com"
    client_options = {"api_endpoint": endpoint_url}
    # Initialize client that will be used to create and send requests
    # This client only needs to be created once, and can be reused for multiple requests
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
 
    # The format of each instance should conform to the deployed model's prediction input schema
    # Here we send the base64-encoded image and image name
    imgb64 = encode_image(cv2.imread(imgpath))
    # imgname = os.path.basename(imgpath)
    imgdict = {
        "content": imgb64,
    }
    instance = json_format.ParseDict(imgdict, Value())
    instances = [instance]
    paramsdict = params
    parameters = json_format.ParseDict(paramsdict, Value())

    # Get the endpoint by project name, endpoint region and ID
    endpoint = client.endpoint_path(
        project=project_name, location=endpoint_region, endpoint=endpoint_id
    )
 
    # Make the prediction
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
 
    # The predictions are a google.protobuf.Value representation of the model's predictions
    print(response)
 
 
if __name__ == "__main__":
    make_prediction(
        imgpath="resource/articles-5266_imagen_01.jpg",
        params={"weight": "10"},
        project_name=PROJECT_ID,
        endpoint_region=REGION,
        endpoint_id=ENDPOINT_ID
    )