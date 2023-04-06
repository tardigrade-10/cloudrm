import torchvision.transforms as transforms
import cv2
import numpy as np
from torch.utils.data import Dataset
import os


transform_128 = transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Resize(128),
                        transforms.CenterCrop(128),
                        ])

transform_512 = transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Resize(512),
                        transforms.CenterCrop(512),
                        ])

def preprocess(image):
    image = cv2.imread(str(image), 1).astype(np.float32)/255
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = transform_512(image)

    return image

def preprocess_app(file):
    image_bytes = file.read()
    image_np = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    image_np = transform_512(image_np)

    return image_np


class TrainDataset(Dataset):
    def __init__(self, train_list, img_dir, lab_dir, transform=None):
        super().__init__()

        self.img_dir = img_dir
        self.lab_dir = lab_dir
        self.imlist = np.loadtxt(train_list, str)
        self.imlist = os.listdir(img_dir)
        self.transform = transform

    def __len__(self):
        return len(self.imlist)
 
    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.imlist[idx])
        image = cv2.imread(img_path, 1).astype(np.float32)/255
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        label_path = os.path.join(self.lab_dir, self.imlist[idx])
        label = cv2.imread(label_path, 1).astype(np.float32)/255
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            image, label = self.transform(image), self.transform(label)
        
        return image, label








