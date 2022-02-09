
import os
from datetime import datetime
from dotenv import load_dotenv

# Load Environment
load_dotenv()
IMAGE_NAME = os.environ['IMAGE_NAME']
PROJECT_ID = os.environ['PROJECT_ID']
tag = datetime.now().strftime("%d%m%y%H%M%S")

os.system(f"docker tag {IMAGE_NAME} gcr.io/{PROJECT_ID}/detectron2:{tag}")
os.system(f"docker push gcr.io/{PROJECT_ID}/detectron2:{tag}")
print(f"pushed ---> gcr.io/{PROJECT_ID}/detectron2:{tag}")