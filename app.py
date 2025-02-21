import streamlit as st
import os
import subprocess

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "trimmed_clips"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

st.title("🎬 Auto Video Trimmer (60-sec Clips)")
st.write("Upload a large video, and it will be automatically split into 1-minute clips.")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file:
    video_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    if not os.path.exists(video_path):
        st.error("❌ File not found after upload. Please try again.")
    else:
        st.success("✅ Video uploaded! Processing...")

        # Check if ffprobe is installed
        ffprobe_check = subprocess.run(["which", "ffprobe"], stdout=subprocess.PIPE, text=True)
        if not ffprobe_check.stdout.strip():
            st.error("❌ ffprobe is not installed or not accessible. Please install it and try again.")
        else:
            # Get video duration using ffprobe
            def get_video_duration(video_path):
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return float(result.stdout.strip()) if result.stdout.strip() else 0

            duration = get_video_duration(video_path)
            if duration == 0:
                st.error("❌ Unable to determine video duration. Please check the file format.")
            else:
                num_clips = int(duration // 60) + (1 if duration % 60 > 0 else 0)
                clip_paths = []

                for i in range(num_clips):
                    start_time = i * 60
                    output_clip = os.path.join(OUTPUT_FOLDER, f"clip_{i+1}.mp4")

                    # Trim using ffmpeg
                    subprocess.run(
                        ["ffmpeg", "-y", "-i", video_path, "-ss", str(start_time), "-t", "60", "-c:v", "copy", "-c:a", "copy", output_clip],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )

                    clip_paths.append(output_clip)

                st.success(f"✅ Video successfully split into {num_clips} clips!")

                # Show download buttons for each clip
                for clip in clip_paths:
                    with open(clip, "rb") as f:
                        st.download_button(f"Download {os.path.basename(clip)}", f, file_name=os.path.basename(clip))
else:
    st.info("📂 Please upload a video to start auto-trimming.")
