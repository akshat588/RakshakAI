"""
===============================================================================
RakshakAI
QR Dataset Loader
===============================================================================
"""

import os
import cv2
import pandas as pd


class QRDatasetLoader:

    def __init__(self, benign_dir, malicious_dir):

        self.benign_dir = benign_dir
        self.malicious_dir = malicious_dir

        self.detector = cv2.QRCodeDetector()

    def decode_qr(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            return None

        data, points, _ = self.detector.detectAndDecode(image)

        if points is None:
            return None

        if data.strip() == "":
            return None

        return data.strip()

    def load_folder(self, folder, label):

        rows = []

        for file in sorted(os.listdir(folder)):

            if not file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp")):
                continue

            path = os.path.join(folder, file)

            content = self.decode_qr(path)

            if content is None:
                continue

            rows.append({"filename": file, "qr_content": content, "label": label})

        return rows

    def build_dataframe(self):

        benign = self.load_folder(self.benign_dir, 0)

        malicious = self.load_folder(self.malicious_dir, 1)

        df = pd.DataFrame(benign + malicious)

        return df


if __name__ == "__main__":

    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]

    loader = QRDatasetLoader(
        benign_dir=str(
            project_root
            / "02_Dataset_Design_Collection"
            / "raw_data"
            / "qr"
            / "benign_qr_images_500"
        ),
        malicious_dir=str(
            project_root
            / "02_Dataset_Design_Collection"
            / "raw_data"
            / "qr"
            / "malicious_qr_images_500"
        ),
    )
    df = loader.build_dataframe()

    print(df.head())

    print()

    print(df["label"].value_counts())

    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]

    dataset_dir = project_root / "03_AI_Model_Development" / "datasets"

    dataset_dir.mkdir(parents=True, exist_ok=True)

    output = dataset_dir / "qr_dataset.csv"

    df.to_csv(output, index=False)

    print(f"Dataset saved to: {output}")

    print(f"Total Samples : {len(df)}")
