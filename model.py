import torch.nn as nn
from torchvision.models import (efficientnet_b3, EfficientNet_B3_Weights)

def get_model(num_classes):
    model = efficientnet_b3(weights=EfficientNet_B3_Weights.DEFAULT)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

    return model