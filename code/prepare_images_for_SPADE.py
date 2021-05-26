import os, sys
from PIL import Image
import math
import glob


def our_clustering(img):
    width = 64
    height = 64
    #width = 2048
    #height = 1024
    color_array = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], [111, 74, 0], [81, 0, 81], [128, 64, 128], [244, 35, 232], [250, 170, 160],
                   [230, 150, 140], [70, 70, 70], [102, 102, 156], [190, 153, 153], [180, 165, 180], [150, 100, 100],
                   [150, 120, 90], [153, 153, 153],[153, 153, 153], [250, 170, 30], [220, 220, 0], [107, 142, 35], [152, 251, 152],
                   [70, 130, 180], [220, 20, 60], [255, 0, 0], [0, 0, 142], [0, 0, 70], [0, 60, 100], [0, 0, 90],
                   [0, 0, 110], [0, 80, 100], [0, 0, 230], [119, 11, 32], [0, 0, 142]]
    length = len(color_array)
    clustering_img = Image.new('RGB', (width, height))
    clustering_img1 = clustering_img.load()
    labelIds_img = Image.new('RGB', (width, height))
    labelIds_img1 = labelIds_img.load()

    j = 0
    while j < height:
        i = 0
        while i < width:
            min_dist = 255
            clustering_img1[i, j] = img[i, j]
            (r, g, b) = img[i, j]
            for x in range(length):
                (r2, g2, b2) = color_array[x]
                dist1 = math.sqrt(pow((r - r2), 2) + pow((g - g2), 2) + pow((b - b2), 2))
                if dist1 < min_dist:
                    clustering_img1[i, j] = (r2, g2, b2)
                    min_dist = dist1
                    labelIds_img1[i, j] = (x, x, x)
            i = i + 1
        j = j + 1
    return clustering_img, labelIds_img


if __name__ == '__main__':
    output = 'data/generated_for_SPADE/gtFine/val/'
    input_dir = 'data/generated_from_styleGAN/'
    input_leftImg_dir = 'data/generated_for_SPADE/leftImg8bit/val/frankfurt/'
    img_array = []
    input_leftImg_dir_array =[]
    i = 0
    for filename in glob.glob(os.path.join(input_leftImg_dir, '*.png')):
        filename_base = os.path.basename(filename)
        filename_saved = '_'.join(filename_base.split('_')[:-2])
        print(filename_saved)
        input_leftImg_dir_array[i] = filename
        i = i + 1
        if (i == 50):
            break

    i=0
    for filename in glob.glob(os.path.join(input_dir, '*.png')):
        img = Image.open(filename, 'r')
#         img = img.resize((64, 64))
#         #img = img.resize((2048, 1024))
#         img.save('img_resize.png')
#         img = Image.open('img_resize.png', 'r')
        print("i = ", i)
        img = img.load()
        clustering_img, labelIds_img = our_clustering(img)
        #filename_base = os.path.basename(filename)
        #filename_saved = '_'.join(filename_base.split('_')[:-2])
        clustering_img.save(output + input_leftImg_dir_array[i] + '_gtFine_color.png', 'PNG')
        labelIds_img.save(output + input_leftImg_dir_array[i] + "_gtFine_labelIds.png", 'PNG')
        i = i+1
        if (i == 50):
            break