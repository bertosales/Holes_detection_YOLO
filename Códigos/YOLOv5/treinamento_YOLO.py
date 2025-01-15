!git clone https://github.com/ultralytics/yolov5  # Clonar repositório YOLOv5
# %cd yolov5
!pip install -r requirements.txt  # Instalar dependências do YOLOv5

import wandb
wandb.init(project="YOLOv5", sync_tensorboard=True)

from google.colab import drive
drive.mount('/content/drive')

!pip install roboflow

from roboflow import Roboflow

rf = Roboflow(api_key="lAPglxJRGAYofgmV1ub6")
project = rf.workspace("yan-bjd5o").project("tcc-tyebp")
version = project.version(3)

dataset = version.download("yolov5")

!ls {dataset.location}
print(dataset.location)

!python train.py --img 640 --batch 16 --epochs 50 --data /content/yolov5/tcc-3/data.yaml --weights yolov5s.pt --project /content/drive/MyDrive/yolov5-training --name run3 --cache


