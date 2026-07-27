import json
import torch
from PIL import Image
from torchvision import transforms
from model import get_model

#device
device = torch.device("cpu")

#Load class names
with open("class_names.json", "r") as f:
    classes = json.load(f)

#Load model
model = get_model(len(classes))
model.load_state_dict(
    torch.load(
        "best_model.pth",
        map_location=device
    )
)
model.to(device)
model.eval()

print("EfficientNet-B3 Loaded Successfully!")
print(f"Number of classes: {len(classes)}")

#Image transforms
transform = transforms.Compose(
    [
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ]
)

def predict_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)
    image = image.to(device)

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

        pokemon_name = classes[
            index.item()
        ]

        confidence = round(
            probability.item() * 100,
            2
        )
        results.append((pokemon_name,confidence))

    #Highest confidence prediction
    prediction = results[0][0]
    confidence = results[0][1]
    return (prediction, confidence, results)