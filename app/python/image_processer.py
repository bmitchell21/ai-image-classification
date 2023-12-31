import torch
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
from torchvision import transforms
from flask import request
import io
import warnings

# function to process image
def process_image(image_file):
    warnings.filterwarnings('ignore')

    # Load the model with pre-trained weights
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model.eval()  # Set the model to evaluation mode

# Convert image file to PIL Image
    image = Image.open(io.BytesIO(image_file.read()))

    # Check if image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Define your transformations
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Apply the transformations to the image
    tensor_image = transform(image)

    # Add a batch dimension
    tensor_image = tensor_image.unsqueeze(0)

    # Feed the tensor image to the model
    prediction = model(tensor_image).squeeze(0).softmax(0)
    class_id = prediction.argmax().item()
    score = prediction[class_id].item()
    category_name = weights.meta["categories"][class_id]
    print(f"{category_name}: {100 * score:.1f}%")

    return (f"Image classification: {category_name}\nChance of accuracy: {100 * score:.1f}%")
