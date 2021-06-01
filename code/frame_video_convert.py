
import cv2
import numpy as np
import glob
import os

def image_seq_to_video(imgs_path, output_path='./video.mp4', fps=15.0):
    output = output_path
    img_array = []
    for filename in glob.glob(os.path.join(imgs_path, '*.png')):
        img = cv2.imread(filename)
        # height, width, layers = img.shape
        img = cv2.resize(img, (662, 332))
        # img = cv2.resize(img, (width, height))
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

        # print(size)
        print("writing video...")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
        out = cv2.VideoWriter(output, fourcc, fps, size)
        # out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        print("saved video @ ", output)


def video_to_image_seq(vid_path, output_path='./datasets/OTB/img/Custom/'):
    os.makedirs(output_path, exist_ok=True)
    vidcap = cv2.VideoCapture(vid_path)
    success, image = vidcap.read()
    count = 0
    print("converting video to frames...")
    while success:
        fname = str(count).zfill(4)
        cv2.imwrite(os.path.join(output_path, fname + ".jpg"), image)  # save frame as JPEG file
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
        count += 1
    print("total frames: ", count)


imgs_path = "./code/StyleGAN/sample_segmantation_map"
image_seq_to_video(imgs_path, output_path='./results/styleGan_samples_process.mp4', fps=30)
# if fps is larger the rate of the video is faster
