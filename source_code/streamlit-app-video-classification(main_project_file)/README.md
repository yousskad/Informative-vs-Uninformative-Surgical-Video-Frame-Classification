

# Surgical vs. Non-Surgical Video Classification Tool

This project provides a browser-based tool for binary classification of surgical and non-surgical videos using a YOLOv11 segmentation model. The interface is built with Streamlit and also the application is containerized with Docker for ease of deployment and scalability.

---

## Project Overview

- **Task**: Binary classification of surgical vs. non-surgical video content  
- **Model**: YOLOv11-seg (medium) fine-tuned on a custom dataset  
- **Interface**: Streamlit-based interactive web application  
- **Deployment Options**: Native Python environment or Docker container  

---

## ⚠️ IMPORTANT NOTES

## PLEASE READ CAREFULLY BEFORE RUNNING THE APPLICATION

---

### 🔹 **Model File (`best-seg.pt`) Not Included in the zip (use all of this repository and ignore all of the zip file)**

- ## [Note: The `best-seg.pt` model file is **NOT** included in the zip but in Github due to file size constraints.]
- ## [Note: The `model-training-files/` directory is **NOT** included in the zip but in Github due to file size constraints.]


### 🔹 **Clone the Complete Repository**

- ## Please clone the **full repository (including model)** from:  
  **`https://github.com/yousskad/Informative-vs-Uninformative-Surgical-Video-Frame-Classification.git`**

### 🔹 **Check Model in Correct Directory**

- Ensure the model file is placed in the project root directory **(open terminal from this directory)**:  
  **`streamlit-app-video-classification/`**


## Folder Structure

> **Note**: Ensure you are inside the `streamlit-app-video-classification/` directory before running the code.

```
streamlit-app-video-classification/
├── app.py               # Streamlit application logic
├── best-seg.pt          # Trained YOLOv11 model weights (not included in repo)
├── requirements.txt     # Python dependencies
└── Dockerfile           # Docker build instructions
```

---

## Python Setup (Local Environment) [Note: create a new env with python3.12 and active it]

### Prerequisites

- Python 3.12 or higher  
- `virtualenv` for environment isolation  

### Steps

1. **Create and activate a virtual environment**

    ```bash
    # Install virtualenv if not already installed
    pip install virtualenv

    # Create virtual environment
    virtualenv venv --python=python3.12

    # Activate (depending on your shell)
    source venv/bin/activate        # bash/zsh
    source venv/bin/activate.fish   # fish
    source venv/bin/activate.csh    # csh/tcsh
    .\venv\Scripts\activate.bat     # Windows cmd
    .\venv\Scripts\Activate.ps1     # PowerShell
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit application**

    ```bash
    streamlit run app.py
    ```

4. **Usage**

    - Open your browser and navigate to: `http://localhost:8501`
    - Upload a video (MP4, AVI, MOV from local computer or dailymotion video surgical or non-surgical videos URL)  
      **Note**: Avoid using YouTube URLs, as surgical videos are often age-restricted and difficult to download.
    - Click on “Process Video URL”
    - The system will display:
      - Predicted class: Surgical or Non-Surgical  
      - Confidence score  
      - Visualization of predicted segmentation overlays

---

## Docker Setup (Containerized Deployment) [Full Alternative]

### Prerequisites

- Docker Engine v20.10 or later  
- NVIDIA GPU with CUDA 12.7 (recommended for good inference acceleration)  
- Docker Hub account (for publishing containers, if needed)  

### Steps

### 🔹 **Run Using Pre-Built Docker Image (Recommended)**

To run the app directly using Docker:

```bash
docker pull crownai/surgical-video-analyzer
```
## or,


1. **Build the Docker image from scratch**

    ```bash
    docker build -t surgical-classifier:latest .
    ```

2. **Run the Docker container**

    ```bash
    docker run -p 8501:8501 --name surgical-app surgical-classifier:latest
    ```

3. **Access the Application**

    Open your browser and navigate to: `http://localhost:8501`

4. **(Optional) Push to Docker Hub**

    ```bash
    docker tag surgical-classifier:latest yourdockerhubusername/surgical-classifier:latest
    docker push yourdockerhubusername/surgical-classifier:latest
    ```

---
```
