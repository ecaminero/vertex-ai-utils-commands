
import os
from datetime import datetime
from dotenv import load_dotenv

# Load Environment
load_dotenv()

IMAGE_NAME = os.environ['LOCAL_IMAGE_NAME']
ARTIFACT_IMAGE_NAME = os.environ['LOCAL_IMAGE_NAME']
PROJECT_ID = os.environ['PROJECT_ID']
MODEL_NAME = os.environ['MODEL_NAME']
REGION = os.environ['PROJECT_REGION']
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

CONTAINER_SERVICE = f"gcr.io/{PROJECT_ID}/{ARTIFACT_IMAGE_NAME}:090222182654"
