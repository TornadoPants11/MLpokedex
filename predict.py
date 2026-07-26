import json
import torch

from PIL import Image
from torchvision import transforms

from model import get_model

device = torch.device("cpu")
with open("class_names.json", "r") as f:
    classes = json.load(f)

model = get_model(len(classes))
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.to(device)
model.eval()

print("EfficientNet-B3 Loaded Successfully!")
print(f"Number of classes: {len(classes)}")

#Load image transform just as training transforms
transform = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

#Prediction function
def predict_image(image_path):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Apply transforms
    image = transform(image)

    # Add batch dimension
    image = image.unsqueeze(0)

    image = image.to(device)

    # Disable gradients
    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        top_probs, top_indices = torch.topk(
            probabilities,
            5
        )

    results = []

    for probability, index in zip(
        top_probs[0],
        top_indices[0]
    ):

        pokemon_name = classes[index.item()]

        confidence = round(
            probability.item() * 100,
            2
        )

        results.append(
            (
                pokemon_name,
                confidence
            )
        )

    return results