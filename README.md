# Creating Segmentation Maps using Style GAN

![](https://www.cityscapes-dataset.com/wordpress/wp-content/uploads/2015/07/zuerich00.png)

### [Project Report (Hebrew)](https://nvlabs.github.io/SPADE/) | [Youtube Demo of styleGAN training process](https://youtu.be/MXWm6w4E5q0)

Students: [Inbal Aharoni](mailto:AHARONINBAL@gmail.com),  [Shani Israelov](mailto:shani1610@gmail.com), Supervised by: [Idan kligvasser](mailto:kligvasser@gmail.com)

The code is released for academic research use only.

## Installation

connect to git repository if did not clone in the first time.
```bash
git remote set-url origin  https://github.com/shani1610/SegmentationMapStyleGan.git
```

## Dataset Preparation

The data directory can be downloaded [here](https://drive.google.com/drive/folders/12W2-Ke5p_asRKctR7YtWLbVLvuGyOGdF?usp=sharing). the original dataset were downloaded [here](https://www.cityscapes-dataset.com/)

The data directory contains the following folders:

* `generated_for_SPADE` - the generated from styleGAN segmantation map after running the script `prepare_for_spade` that clustering the in-between pixels to values that correspond to the [cityscape classes](https://github.com/mcordts/cityscapesScripts/blob/master/cityscapesscripts/helpers/labels.py) and generate the label maps that required for running the SPADE modoule. 

* `generated_from_SPADE`

* `generated_from_styleGAN` - the generated segmantation maps.

* `original_coarse` - the data coarse was used for the DCGAN part because it requires a lot more data then fine images number. 

* `original_for_SPADE` - you can also ran the SPADE on the original data and get full size image. 

* `original_gtFine` - this is used in the styleGAN part.

* `original_leftImg8bit` - the realistic images.

* `original_leftImg8bit_prepared_for_styleGAN` - the LMDB files required for the styleGAN training. 

* `prepared_for_styleGAN` - the LMDB files required for the styleGAN training. 

## StyleGAN

1) prepare the data:

   ```bash
   python code/StyleGAN/prepare_data.py --out data/prepared_for_styleGAN/LMDB_PATH --n_worker 1 data/original_gtFine
   ```
   
   This will convert images to jpeg and pre-resizes it, Then you can train StyleGAN.
   
   You can use our LMDB files which included in the data directory in `prepared_for_styleGAN` folder. 

2) train:

    ```bash
    python code/StyleGAN/train.py data/prepared_for_styleGAN/LMDB_PATH
    ```
    
    this generate the model in the checkpoint directory and a samples directory which is stored in the data directory in the generated_from_styleGAN.
    
    You can use our checkpoint directory that can be download [here](https://drive.google.com/drive/folders/1c550S68Q_17frHlmM6qF125gwOzOsPeL?usp=sharing). extract this .zip in `code/StyleGAN/checkpoint`.

3) generate new images after training:

   ```bash
    python code/StyleGAN/generate.py code/StyleGAN/checkpoint/train_step-5.model --size 64
    ```
    make sure `--size` is corresponding to the size of the train_step-*.model .

## SPADE
 
1) generate new images from the original cityscape dataset:
```bash
  python code/SPADE/test.py --name cityscapes_pretrained/ --dataset_mode cityscapes --dataroot data/original_for_SPADE/ --batchSize  8
  ```
  if a CUDA memory limit occure try to use smaller `--batchSize`.

2) generate new images from the dataset that were generated by the styleGAN:

```bash
  python code/SPADE/test.py --name cityscapes_pretrained/ --dataset_mode cityscapes --dataroot data/generated_for_SPADE/ --batchSize 4 --no_instance --label_nc 36 --no_pairing_check
       --crop_size 64 --load_size 64
  ```
  
## Evaluation

you can find the relavent files in `code/FID`.

```bash
python code/FID/fid_score.py path/to/dataset1 path/to/dataset2
```

## Acknowledgments

This code borrows heavily from [style-based-gan-pytorch](https://github.com/rosinality/style-based-gan-pytorch) and [SPADE](https://github.com/NVlabs/SPADE). We thank the creators. 
