import torch
from model import AutoencoderModel
import cv2
from data import preprocess
import argparse
import os


def predict(args):

    model = AutoencoderModel()

    input_path = args.image
    weights_path = "weights\model_state_dict_512.pt"

    img = preprocess(input_path)

    if args.gpu:
        device = torch.device('cuda:0')
        model = model.to(device)
        img = img.to(device)

    model.load_state_dict(torch.load(weights_path))
    model.eval()

    out = model(img)
    out = out.detach().cpu().numpy().transpose(1, 2, 0) * 255.0

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    cv2.imwrite(os.path.join(args.out_dir, "out.jpeg"), out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--out_dir', type=str, required=True, default='results')
    parser.add_argument('--gpu', type=bool, default=False)

    args = parser.parse_args()

    predict(args)


