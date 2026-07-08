"""
===============================================================================
RakshakAI
Deepfake Dataset Loader
===============================================================================
"""

from pathlib import Path

from torchvision import datasets
from torchvision import transforms
from torch.utils.data import random_split, DataLoader

IMAGE_SIZE = 224
BATCH_SIZE = 32


def get_dataloaders():

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = (
        project_root / "02_Dataset_Design_Collection" / "raw_data" / "deepfake"
    )

    transform = transforms.Compose(
        [
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(
                brightness=0.2,
                contrast=0.2,
                saturation=0.2,
            ),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    dataset = datasets.ImageFolder(
        root=str(dataset_path),
        transform=transform,
    )

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    train_dataset, val_dataset = random_split(
        dataset,
        [train_size, val_size],
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
    )

    return (
        train_loader,
        val_loader,
        dataset.classes,
    )


if __name__ == "__main__":

    train_loader, val_loader, classes = get_dataloaders()

    print("=" * 60)
    print("Classes :", classes)
    print("Train batches :", len(train_loader))
    print("Validation batches :", len(val_loader))
    print("=" * 60)
