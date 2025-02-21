import cv2
import os

def process_video(input_path, trim_duration=60):
    try:
        cap = cv2.VideoCapture(input_path)

        if not cap.isOpened():
            raise ValueError("Could not open video file")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames // fps  

        output_files = []
        segment_count = (duration // trim_duration) + 1  

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        for i in range(segment_count):
            output_file = f"output/trimmed_{i+1}.mp4"
            out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

            for _ in range(fps * trim_duration):  
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            out.release()
            output_files.append(output_file)

        cap.release()
        return output_files

    except Exception as e:
        print(f"Error processing video: {e}")
        return None
