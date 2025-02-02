import time
import configparser
from pathlib import Path
from PIL import Image, ImageOps

DEBUG = False
END = 100000000  # max number of images to process
SKIP = 0 # 5000

def run_simulator(
    input_dir, imgs, output_dir="./imgs", ext="png", step=1, sleep=0.1, equalize=False, n_camera=1,
):
    print(len(imgs))
    for i in range(len(imgs)):
        if i < SKIP:
            continue
        if i == END:
            print(
                f"Processed {END} images. Change the END variable in simulator.py to process more."
            )
            quit()

        # Process only every STEP-th image
        if i % step != 0:
            continue

        if DEBUG:
            print(f"processing {i}-th img ({i}/{len(imgs)})")

        for c in reversed(range(n_camera)):

            im_name = imgs[i].name
            #im_name = im_name[8:] # for ant3d
            im = Image.open(input_dir / f"cam{c}/data" / im_name)
            #im = Image.open(input_dir / f"cam{c}/data" / f"ANT3D_{c+1}_{im_name}") # for ant3d
            rgb_im = im.convert("RGB")
            if equalize == True:
                rgb_im = ImageOps.equalize(rgb_im)
            #rgb_im.thumbnail((960, 600), Image.Resampling.LANCZOS) # for ant3d

            # make sure the output folder exist
            dp_cam = Path(output_dir) / f"cam{c}"
            dp_cam.mkdir(exist_ok=True, parents=True)
            # ---------------------------------
            rgb_im.save(Path(output_dir) / f"cam{c}" / f"{Path(im_name).stem}.{ext}")
            time.sleep(sleep)

    print("No more images available")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config_4_run_tot_2000.ini", encoding="utf-8")
    input_dir = Path(config["DEFAULT"]["SIMULATOR_IMG_DIR"])
    output_dir = config["DEFAULT"]["OUTPUT_IMGS_DIR"]
    ext = config["DEFAULT"]["IMG_FORMAT"]
    step = int(config["DEFAULT"]["STEP"])
    sleep = float(config["DEFAULT"]["SIMULATOR_SLEEP_TIME"])
    equalize = config["DEFAULT"].getboolean("EQUALIZE")
    n_camera = int(config["CALIBRATION"]["N_CAMERAS"])
    from pathlib import Path
    dp_out = Path(output_dir)
    if not dp_out.exists():
        dp_out.mkdir(exist_ok=True, parents=True)
    path_to_kfrms_cam0 = Path(input_dir /"cam0/data")
    if not path_to_kfrms_cam0.exists():
        print(
            '\nERROR: Keyframe directory cam0:', 
            Path(input_dir / "cam0/data"), 
            '\nKeframe dir do not exist, check the input path:',
            '\nExpected dir structures:'
            '\ninput_path',
            '\n--> cam0',
            '\n----> data',
            '\n------> 00000.jpg',
            )

    imgs = sorted(Path(input_dir / "cam0/data").glob("*"))
    run_simulator(input_dir, imgs, output_dir, ext, step, sleep, equalize, n_camera)
