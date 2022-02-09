import os
from google.cloud import aiplatform
from google.cloud.aiplatform import Model, Endpoint
from dotenv import load_dotenv

# Load Environment
load_dotenv()

PROJECT_ID = os.environ['PROJECT_ID']
REGION = os.environ['PROJECT_REGION']
PROJECT_ID = os.environ['PROJECT_ID']
MODEL_NAME = os.environ['MODEL_NAME']
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

CONTAINER_SERVICE = "gcr.io/{PROJECT_ID}/detectron2:090222182654"
aiplatform.init(project=PROJECT_ID, location=REGION)


print("----------------- Create model ----------------")
# Create model
models = Model.list(filter=f'displayName="{MODEL_NAME}"')
if models:
    model = models[0]
else:
    model = aiplatform.Model.upload(
        display_name=MODEL_NAME,
        serving_container_image_uri=CONTAINER_SERVICE,
        serving_container_predict_route="/inference",
        serving_container_health_route="/health",
        serving_container_environment_variables={"PORT": "8000"},
        serving_container_ports=[8000],
        sync=True,
    )
    model.wait()

print("Model:")
print(f"\tDisplay name: {model.display_name}")
print(f"\tResource name: {model.resource_name}")

print("----------------- Create Endpoint ----------------")
# Create Endpoint
endpoints = Endpoint.list(filter=f'displayName="{ENDPOINT_NAME}"')

if endpoints:
    endpoint = endpoints[0]
else:
    print(f"Endpoint {ENDPOINT_NAME} doesn't exist, creating...".format())
    endpoint = aiplatform.Endpoint.create(display_name=ENDPOINT_NAME)

print("Endpoint:")
print(f"\tDisplay name: {endpoint.display_name}")
print(f"\tResource name: {endpoint.resource_name}")

print("----------------- Deploy Model ----------------")
# Deploy Model
model.deploy(
    endpoint=endpoint,
    deployed_model_display_name=MODEL_NAME,
    traffic_percentage=100,
    machine_type="n1-standard-4",
    min_replica_count=1,
    max_replica_count=1,
    accelerator_type="NVIDIA_TESLA_K80",
    accelerator_count=1,
    sync=True,
)
print(f"Model {model.display_name} deployed at endpoint {endpoint.display_name}.")
