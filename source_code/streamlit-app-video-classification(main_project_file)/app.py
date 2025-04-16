import streamlit as st
import cv2
import os
import yt_dlp
from ultralytics import YOLO

# Load YOLO model
model = YOLO('best-seg.pt')

def download_video(url):
    """Download video using yt-dlp and return path"""
    ydl_opts = {
        'outtmpl': 'temp_video.%(ext)s',
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def extract_screenshots(video_path, num_screenshots=20):
    """Extract screenshots at equal intervals"""
    cap = cv2.VideoCapture(video_path)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    interval = duration / num_screenshots
    
    screenshots = []
    for i in range(1, num_screenshots + 1):
        cap.set(cv2.CAP_PROP_POS_MSEC, (interval * i) * 1000)
        ret, frame = cap.read()
        if ret:
            path = f"screenshot_{i}.jpg"
            cv2.imwrite(path, frame)
            screenshots.append(path)
    cap.release()
    return screenshots

st.title("Surgical Video Analyzer")

# Input method selection
input_method = st.selectbox(
    "Select input method:",
    ("Video URL", "File Upload")
)

if input_method == "Video URL":
    url = st.text_input("Enter Dailymotion Surgery Video URL:")
    process_button = st.button("Process Video URL")
elif input_method == "File Upload":
    video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
    process_button = st.button("Process Uploaded File")

if process_button:
    try:
        video_path = None
        surgical_images = 0
        non_surgical_images = 0
        results_data = []  # To store results for later display

        # Handle URL input
        if input_method == "Video URL" and url:
            with st.spinner("Downloading video..."):
                video_path = download_video(url)
        
        # Handle file upload
        elif input_method == "File Upload" and video_file:
            video_path = "temp_uploaded_video.mp4"
            with open(video_path, "wb") as f:
                f.write(video_file.read())
        
        if video_path:
            # Common processing for both methods
            with st.spinner("Processing video..."):
                screenshots = extract_screenshots(video_path)
                
                # Process all screenshots first
                for screenshot in screenshots:
                    results = model.predict(screenshot)
                    annotated = results[0].plot()
                    
                    detections = []
                    surgical_detected = False
                    non_surgical_detected = False
                    
                    for box in results[0].boxes:
                        class_name = model.names[int(box.cls)]
                        confidence = box.conf.item()
                        detections.append(f"{class_name} ({confidence:.2f})")
                        
                        if class_name in ['surgical-area', 'surgical-tool']:
                            surgical_detected = True
                        if class_name in ['image', 'person', 'text']:
                            non_surgical_detected = True
                    
                    if surgical_detected:
                        surgical_images += 1
                    if non_surgical_detected:
                        non_surgical_images += 1
                    
                    # Store results for later display
                    results_data.append({
                        'original': screenshot,
                        'annotated': annotated,
                        'detections': detections
                    })

            # Show classification first
            st.header("Final Video Classification")
            if surgical_images >= 10:
                st.success(f"**Surgical Video** (Detected surgical elements in {surgical_images}/20 images)")
            elif non_surgical_images >= 10:
                st.success(f"**Non-Surgical Video** (Detected non-surgical elements in {non_surgical_images}/20 images)")
            else:
                st.warning(f"**Inconclusive** (Surgical elements: {surgical_images}/20, Non-surgical elements: {non_surgical_images}/20)")
            
            # Show detailed results after classification
            st.header("Detailed Analysis Results")
            for idx, result in enumerate(results_data, 1):
                cols = st.columns(2)
                
                with cols[0]:
                    st.image(result['original'], caption=f"Original Screenshot {idx}")
                
                with cols[1]:
                    st.image(result['annotated'], caption="YOLO Detection")
                    if result['detections']:
                        st.write("Detected:")
                        st.write("\n".join(result['detections']))
                    else:
                        st.write("No detections found")

            # Cleanup
            os.remove(video_path)
            for screenshot in screenshots:
                os.remove(screenshot)
        
        else:
            st.warning("Please provide valid input based on your selected method")
    
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        if video_path and os.path.exists(video_path):
            os.remove(video_path)