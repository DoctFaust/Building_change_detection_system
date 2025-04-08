import os
import sys
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import transforms
from .change_detection_model import SNUNet_ECAM
import cv2

def predict_changes(imgA_path, imgB_path, model_path=None, output_path=None):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    img_size = 256
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    
    if model_path is None:
        current_dir = os.path.dirname(os.path.dirname(sys.executable))
        model_path = os.path.join(current_dir, "model", "model.pth")
    
    if output_path is None:
        project_root = os.path.dirname(os.path.dirname(sys.executable))
        output_dir = os.path.join(project_root, "result")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "result_image.png")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    model = SNUNet_ECAM(in_ch=3, out_ch=1)
    
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
    except Exception as e:
        raise Exception(f"Failed to load model from {model_path}: {str(e)}")
    
    model.to(device)
    model.eval()
    
    preprocess = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])
    
    try:
        imgA = Image.open(imgA_path).convert("RGB")
        imgB = Image.open(imgB_path).convert("RGB")
    except Exception as e:
        raise Exception(f"Failed to open images: {str(e)}")
    
    tensorA = preprocess(imgA).unsqueeze(0).to(device)
    tensorB = preprocess(imgB).unsqueeze(0).to(device)
    
    with torch.no_grad():
        logits = model(tensorA, tensorB)
        prob_map = torch.sigmoid(logits).squeeze().cpu().numpy()
        change_mask = (prob_map > 0.5).astype(np.uint8) * 255
    
    change_mask = cv2.resize(change_mask, (1024, 1024), interpolation=cv2.INTER_CUBIC)
    
    result_img = Image.fromarray(change_mask)
    result_img.save(output_path)
    
    return result_img