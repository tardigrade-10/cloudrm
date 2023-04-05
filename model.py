import torch.nn as nn
import torch
import os


class AutoencoderModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding='same')
        self.conv2 = nn.Conv2d(64, 64, 3, padding='same')
        self.conv3 = nn.Conv2d(64, 128, 3, padding='same')
        self.conv4 = nn.Conv2d(128, 128, 3, padding='same')
        self.conv5 = nn.Conv2d(128, 256, 3, padding='same')
        self.conv6 = nn.Conv2d(256, 128, 3, padding='same')
        self.conv7 = nn.Conv2d(128, 128, 3, padding='same')
        self.conv8 = nn.Conv2d(128, 64, 3, padding='same')
        self.conv9 = nn.Conv2d(64, 64, 3, padding='same')
        self.conv10 = nn.Conv2d(64, 3, 3, padding='same')
        self.convt1 = nn.ConvTranspose2d(256, 256, 4, 2, 1)
        self.convt2 = nn.ConvTranspose2d(128, 128, 4, 2, 1)

        self.relu = nn.ReLU(True)
        self.maxpool = nn.MaxPool2d(2)
        self.upsample = nn.Upsample(scale_factor = 2, mode = 'bilinear')
        

    def forward(self, x):

    #encoder
        x = self.relu(self.conv1(x))
        x1 = self.relu(self.conv2(x))
        x = self.maxpool(x1)
        x = self.relu(self.conv3(x))
        x2 = self.relu(self.conv4(x))
        x = self.maxpool(x2)
        x = self.relu(self.conv5(x))

    #decoder
        # x = self.upsample(x)
        x = self.relu(self.convt1(x))
        x = self.relu(self.conv6(x))
        x3 = self.relu(self.conv7(x))
        x = torch.add(x2, x3)
        # x = self.upsample(x)
        x = self.relu(self.convt2(x))
        x = self.relu(self.conv8(x))
        x4 = self.relu(self.conv9(x))
        x = torch.add(x1, x4)
        out = self.relu(self.conv10(x))

        return out
    


class AutoencoderModel_BIG(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding='same')
        self.conv2 = nn.Conv2d(64, 64, 3, padding='same')
        self.conv3 = nn.Conv2d(64, 128, 3, padding='same')
        self.conv4 = nn.Conv2d(128, 128, 3, padding='same')
        self.conv5 = nn.Conv2d(128, 256, 3, padding='same')
        self.conv6 = nn.Conv2d(256, 128, 3, padding='same')
        self.conv7 = nn.Conv2d(128, 128, 3, padding='same')
        self.conv8 = nn.Conv2d(128, 64, 3, padding='same')
        self.conv9 = nn.Conv2d(64, 64, 3, padding='same')
        self.conv10 = nn.Conv2d(64, 3, 3, padding='same')
        self.convt1 = nn.ConvTranspose2d(256, 256, 4, 2, 1)
        self.convt2 = nn.ConvTranspose2d(128, 128, 4, 2, 1)

        self.relu = nn.ReLU(True)
        self.maxpool = nn.MaxPool2d(2)
        self.upsample = nn.Upsample(scale_factor = 2, mode = 'bilinear')
        

    def forward(self, x):

    #encoder
        x = self.relu(self.conv1(x))
        x1 = self.relu(self.conv2(x))
        x = self.maxpool(x1)
        x = self.relu(self.conv3(x))
        x2 = self.relu(self.conv4(x))
        x = self.maxpool(x2)
        x = self.relu(self.conv5(x))

    #decoder
        # x = self.upsample(x)
        x = self.relu(self.convt1(x))
        x = self.relu(self.conv6(x))
        x3 = self.relu(self.conv7(x))
        x = torch.add(x2, x3)
        # x = self.upsample(x)
        x = self.relu(self.convt2(x))
        x = self.relu(self.conv8(x))
        x4 = self.relu(self.conv9(x))
        x = torch.add(x1, x4)
        out = self.relu(self.conv10(x))

        return out
    

def load_model():
    model = AutoencoderModel()
    weights_path = os.path.join(os.getcwd(), 'weights/model_state_dict_512.pt')
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    return model