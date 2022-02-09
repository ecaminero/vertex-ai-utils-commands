import os
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
from google.cloud.aiplatform import Model, Endpoint
from dotenv import load_dotenv

# Load Environment
load_dotenv()

PROJECT_ID = os.environ['PROJECT_ID']
REGION = os.environ['PROJECT_REGION']
MODEL_NAME = os.environ['MODEL_NAME']
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
CONTAINER_SERVICE = "gcr.io/{PROJECT_ID}/detectron2:090222182654"

def undeploy_model_in_endpoint(
    end_point: str,
    project: str,
    model_id: str,
    api_endpoint: str = "us-east1-aiplatform.googleapis.com",
    timeout: int = 7200,
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.EndpointServiceClient(client_options=client_options)
    client_model = aiplatform_v1.services.model_service.ModelServiceClient(client_options=client_options)

    # Get deployed_model_id
    model_name = f'projects/{project}/locations/{REGION}/models/{model_id}'
    model_request = aiplatform_v1.types.GetModelRequest(name=model_name)
    model_info = client_model.get_model(request=model_request)
    deployed_models_info = model_info.deployed_models
    deployed_model_id=deployed_models_info[0].deployed_model_id

    name=f'projects/{project}/locations/{REGION}/endpoints/{end_point}'

    undeploy_request = aiplatform_v1.types.UndeployModelRequest(endpoint=name,deployed_model_id=deployed_model_id)
    client.undeploy_model(request=undeploy_request)


print("----------------- Delete Endpoint ----------------")

undeploy_model_in_endpoint(
    end_point='4680401097116876800',
    model_id='8282225267850608640',
    project=PROJECT_ID
)

print("----------------- Deleted ----------------")
