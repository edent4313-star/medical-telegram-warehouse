from ultralytics import YOLO
from pathlib import Path
import pandas as pd
import logging

# ==================================================
# Logging
# ==================================================

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/yolo_detect.log"),
        logging.StreamHandler()
    ]
)

# ==================================================
# Load YOLOv8 Nano
# ==================================================

model = YOLO("yolov8n.pt")

# ==================================================
# Image Location
# ==================================================

IMAGE_DIR = Path("data/raw/images")

results_list = []

# ==================================================
# Classification Logic
# ==================================================

def classify_image(detected_objects):

    has_person = "person" in detected_objects

    product_objects = [
        "bottle",
        "cup",
        "bowl",
        "box"
    ]

    has_product = any(
        obj in detected_objects
        for obj in product_objects
    )

    if has_person and has_product:
        return "promotional"

    elif has_product and not has_person:
        return "product_display"

    elif has_person and not has_product:
        return "lifestyle"

    return "other"

# ==================================================
# Scan Images
# ==================================================

image_files = list(
    IMAGE_DIR.rglob("*.jpg")
)

logging.info(
    f"Found {len(image_files)} images"
)

for image_path in image_files:

    try:

        result = model(str(image_path))[0]

        detected_objects = []

        max_conf = 0

        for box in result.boxes:

            cls_id = int(box.cls)

            obj_name = model.names[cls_id]

            confidence = float(box.conf)

            detected_objects.append(obj_name)

            max_conf = max(
                max_conf,
                confidence
            )

        image_category = classify_image(
            detected_objects
        )

        # Extract message_id from image filename

        message_id = image_path.stem

        channel_name = image_path.parent.name

        results_list.append({

            "message_id": message_id,

            "channel_name": channel_name,

            "image_path": str(image_path),

            "detected_objects":
                ",".join(
                    detected_objects
                ),

            "confidence_score":
                round(
                    max_conf,
                    4
                ),

            "image_category":
                image_category

        })

    except Exception as e:

        logging.error(
            f"Error processing "
            f"{image_path}: {e}"
        )

# ==================================================
# Save CSV
# ==================================================

df = pd.DataFrame(
    results_list
)

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    "data/processed/"
    "image_detections.csv"
)

df.to_csv(
    output_file,
    index=False
)

logging.info(
    f"Saved {len(df)} detections "
    f"to {output_file}"
)