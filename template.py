import os
from pathlib import Path

def create_folder(path):
    """Create a folder if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"Created folder: {path}")

def create_file(path, content=""):
    """Create a file with optional starter content."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created file: {path}")

def main():

    print("\nCreating Uber Price Prediction Project Structure...\n")

    # ---- FOLDERS ----
    folders = [
        "configs",
        "data/raw",
        "data/interim",
        "data/processed",
        "notebooks",
        "src/collectors",
        "src/pipeline",
        "src/model",
        "src/visualization",
        "scripts",
        "logs"
    ]

    for folder in folders:
        create_folder(folder)

    # ---- FILES ----
    create_file("README.md", "# Uber Price Prediction Project\n")
    create_file("LICENSE", "Add your license text here.\n")
    create_file(".gitignore", "data/raw/\ndata/interim/\n__pycache__/\n")

    create_file("requirements.txt",
        "numpy\npandas\nscikit-learn\nrequests\npyyaml\nmatplotlib\n")

    create_file("configs/config.yaml",
        "google_maps_api_key: ''\nopenweather_api_key: ''\n")

    # empty notebooks
    create_file("notebooks/01_exploration.ipynb")
    create_file("notebooks/02_model_dev.ipynb")

    # src init files
    create_file("src/__init__.py")
    create_file("src/collectors/__init__.py")
    create_file("src/pipeline/__init__.py")
    create_file("src/model/__init__.py")
    create_file("src/visualization/__init__.py")

    # placeholder source code files
    create_file("src/collectors/maps_api.py",
        "# Maps API collector placeholder\n")

    create_file("src/collectors/weather_api.py",
        "# Weather API collector placeholder\n")

    create_file("src/collectors/pricing_simulator.py",
        "# Pricing simulator placeholder\n")

    create_file("src/pipeline/data_collector.py",
        "# Data collector logic placeholder\n")

    create_file("src/pipeline/feature_engineer.py",
        "# Feature engineering logic placeholder\n")

    create_file("src/pipeline/dataset_builder.py",
        "# Dataset builder placeholder\n")

    create_file("scripts/collect_data.py",
        "# Script to collect data\n")

    create_file("scripts/process_data.py",
        "# Script to process data\n")

    create_file("scripts/train_model.py",
        "# Script to train model\n")

    print("\nProject setup complete!")

if __name__ == "__main__":
    main()