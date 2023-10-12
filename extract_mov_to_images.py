import cv2
from tqdm import tqdm


def video_to_frames(fp_video, dp_output):
    # Open the video file
    video = cv2.VideoCapture(fp_video.as_posix())

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    with tqdm(total=total_frames) as pbar:  # create a progress bar
        frame_counter = 0
        while True:
            # Read one frame from the video
            success, frame = video.read()
            if not success:
                break

            # Save this frame into a .png file
            cv2.imwrite(f'{dp_output.as_posix()}/{frame_counter:05}.png', frame)
            frame_counter += 1
            pbar.update(1)  # update the progress bar

    # Close the video file
    video.release()


if __name__ == "__main__":
    from pathlib import Path
    fp_video = Path("C:/Users/xuanl\Desktop\GX010227.mov") # replace with your .mov file path
    dp_output = Path("D:\SfM_Calib\data/sfm_4_run_oct_9")  # replace with your output directory
    video_to_frames(fp_video, dp_output)
