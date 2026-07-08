"""
===============================================================================
RakshakAI
Deepfake Detector Training
PyTorch + ResNet18
===============================================================================
"""

from pathlib import Path
import copy
import time
import sys

import torch
import torch.nn as nn
import torch.optim as optim

from torchvision.models import (
    resnet18,
    ResNet18_Weights,
)

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from utils.deepfake_dataset_loader import get_dataloaders

# =============================================================================
# Configuration
# =============================================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

EPOCHS = 15
LEARNING_RATE = 1e-4
PATIENCE = 4

MODEL_DIR = (
    Path(__file__).resolve().parents[2]
    / "03_AI_Model_Development"
    / "saved_models"
    / "vision"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MODEL_PATH = MODEL_DIR / "deepfake_detector.pth"


# =============================================================================
# Training
# =============================================================================


def train():

    train_loader, val_loader, classes = get_dataloaders()

    print("=" * 70)
    print("Device :", DEVICE)
    print("Classes:", classes)
    print("Train batches:", len(train_loader))
    print("Validation batches:", len(val_loader))
    print("=" * 70)

    weights = ResNet18_Weights.DEFAULT

    model = resnet18(weights=weights)

    in_features = model.fc.in_features

    model.fc = nn.Linear(
        in_features,
        2,
    )

    model = model.to(DEVICE)

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=2,
    )

    best_accuracy = 0.0

    best_weights = copy.deepcopy(model.state_dict())

    patience_counter = 0

    training_start = time.time()

    print("\n")
    print("=" * 70)
    print("Starting Training...")
    print("=" * 70)

    for epoch in range(EPOCHS):

        print(f"\nEpoch {epoch+1}/{EPOCHS}")

        # -------------------------------------------------

        model.train()

        running_loss = 0.0
        running_correct = 0
        total = 0

        for images, labels in train_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(
                outputs,
                labels,
            )

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            _, predicted = torch.max(
                outputs,
                1,
            )

            total += labels.size(0)

            running_correct += (predicted == labels).sum().item()

        train_loss = running_loss / len(train_loader)

        train_accuracy = 100 * running_correct / total

        # -------------------------------------------------

        model.eval()

        val_loss = 0.0

        val_correct = 0

        total_val = 0

        predictions = []

        ground_truth = []

        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(DEVICE)
                labels = labels.to(DEVICE)

                outputs = model(images)

                loss = criterion(
                    outputs,
                    labels,
                )

                val_loss += loss.item()

                _, predicted = torch.max(
                    outputs,
                    1,
                )

                total_val += labels.size(0)

                val_correct += (predicted == labels).sum().item()

                predictions.extend(predicted.cpu().numpy())

                ground_truth.extend(labels.cpu().numpy())

        val_loss /= len(val_loader)

        val_accuracy = 100 * val_correct / total_val

        scheduler.step(val_loss)

        print(f"Train Loss : {train_loss:.4f}")
        print(f"Train Acc  : {train_accuracy:.2f}%")

        print(f"Val Loss   : {val_loss:.4f}")
        print(f"Val Acc    : {val_accuracy:.2f}%")

        if val_accuracy > best_accuracy:

            best_accuracy = val_accuracy

            best_weights = copy.deepcopy(model.state_dict())

            torch.save(
                best_weights,
                MODEL_PATH,
            )

            patience_counter = 0

            print("✓ Best model saved.")

        else:

            patience_counter += 1

            print(f"No improvement ({patience_counter}/{PATIENCE})")

        if patience_counter >= PATIENCE:

            print("\nEarly stopping activated.")

            break

    training_time = (time.time() - training_start) / 60

    model.load_state_dict(best_weights)

    print("\n")
    print("=" * 70)
    print("Training Finished")
    print("=" * 70)

    print(f"Training Time : {training_time:.2f} minutes")

    print(f"Best Validation Accuracy : {best_accuracy:.2f}%")

    # ============================================================
    # Final Evaluation
    # ============================================================

    print("\n")
    print("=" * 70)
    print("Evaluating Best Model...")
    print("=" * 70)

    model.eval()

    predictions = []
    ground_truth = []

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            predictions.extend(predicted.cpu().numpy())

            ground_truth.extend(labels.numpy())

    print("\nClassification Report\n")

    print(
        classification_report(
            ground_truth,
            predictions,
            target_names=classes,
            digits=4,
        )
    )

    print("\nConfusion Matrix\n")

    print(
        confusion_matrix(
            ground_truth,
            predictions,
        )
    )

    # ============================================================
    # Save Final Model
    # ============================================================

    checkpoint = {
        "model_state_dict": model.state_dict(),
        "classes": classes,
        "image_size": 224,
        "architecture": "resnet18",
        "best_validation_accuracy": best_accuracy,
    }

    torch.save(
        checkpoint,
        MODEL_PATH,
    )

    print("\n")
    print("=" * 70)
    print("Deepfake Model Saved Successfully")
    print("=" * 70)

    print(f"Model Path : {MODEL_PATH}")

    print("=" * 70)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    train()
