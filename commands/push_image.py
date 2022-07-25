
import os
from datetime import datetime
from dotenv import load_dotenv

tag = datetime.now().strftime("%d%m%y%H%M%S")
########### CONFIG BLOCK ###########33
# Load Environment
load_dotenv()

IMAGE_NAME = os.environ['IMAGE_NAME']
ARTIFACT_IMAGE_NAME = os.environ['ARTIFACT_IMAGE_NAME']
PROJECT_ID = os.environ['PROJECT_ID']
MODEL_NAME = os.environ['MODEL_NAME']
REGION = os.environ['PROJECT_REGION']
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

CONTAINER_SERVICE = f"gcr.io/{PROJECT_ID}/{ARTIFACT_IMAGE_NAME}:{tag}"
########### CONFIG BLOCK ###########


os.system(f"docker tag {IMAGE_NAME} gcr.io/{PROJECT_ID}/{ARTIFACT_IMAGE_NAME}:{tag}")
os.system(f"docker push gcr.io/{PROJECT_ID}/{ARTIFACT_IMAGE_NAME}:{tag}")
print(f"pushed ---> gcr.io/{PROJECT_ID}/{ARTIFACT_IMAGE_NAME}:{tag}")