# Deep t2i
> My Experients of text to image using deep learning


Generate 256x256 bird image from natural text.

## Data

Main data:
* [CUB-200](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html)
* [Birds Captions from AttnGAN](https://drive.google.com/open?id=1O_LtUP9sch09QH3s_EBAgLEctBQ5JBSJ)

The files with name "anime_heads" are related to another data. Which is a very simple task that try to generate anime faces from just two factors: hair color and eye color. I just use this data to quickly check the functionality of my model. It should work perfectly with this simple task.
* [Simple anime faces data](https://drive.google.com/uc?export=download&id=1tpW7ZVNosXsIAWu8-f5EpwtF3ls3pb79)
* This data is from this [course](http://speech.ee.ntu.edu.tw/~tlkagk/courses_MLDS18.html) 

## Model Architecture

DAMSM
<img src="nbs/images/DAMSM_arch.jpg" width="625" height="476">
<img src="nbs/images/DAMSM_train.jpg" width="625" height="476">

GAN
<img src="nbs/images/GAN_arch.jpg" width="1248" height="476">
<img src="nbs/images/GAN_train.jpg" width="625" height="476">

The architecture design is largely inspired by Attn-GAN, MSG-GAN, SA-GAN and Pro-GAN.

1. Skip connection from MSG-GAN
2. Attention and DAMSM from AttnGAN, 
3. SelfAtten, Spectral norm, Batch Norm from SAGAN
4. Architecture and ema generator from ProGAN but add some residual and attention

Please check this notebook to get more details of my model architecture. ( [03a_model.ipynb](nbs/03a_model.ipynb) )

Check these notebooks to get details of the loss and training. ( [04a_trainer_DAMSM.ipynb](nbs/04a_trainer_DAMSM.ipynb), [04b_trainer_GAN.ipynb](nbs/04b_trainer_GAN.ipynb) )

## Training and Result

Please check these notebooks which contain the full training process. 
([99a_Train_Anime_Heads_DAMSM.ipynb](nbs/99c_Train_Birds_DAMSM.ipynb), [99b_Train_Anime_Heads_GAN.ipynb](nbs/99d_Train_Birds_GAN.ipynb), [99c_Train_Birds_DAMSM.ipynb](nbs/99c_Train_Birds_DAMSM.ipynb), [99d_Train_Birds_GAN.ipynb](nbs/99d_Train_Birds_GAN.ipynb) )


Selected sample results:
<img src="nbs/images/anime_heads_result.jpg" width="300" height="200">
<img src="nbs/images/birds_result.jpg">

You can check [birds_results](https://drive.google.com/file/d/1ZtjY0zswy37DDxHV0JvLhawhthP9ae1M/view?usp=sharing)  or [anime_heads_results](https://drive.google.com/file/d/1PqbnvfK_aha0Pqge16ETLrr7TqNC-xxM/view?usp=sharing) to get the result images during training process for each epoch.

## Pretrained Model

[Exported Anime Face Model](https://drive.google.com/file/d/1pp696JJCD5ng3C7klhHS5Q7_iTKtEpjs/view?usp=sharing)  
[Exported Birds Model](https://drive.google.com/file/d/1phNW_utePcz188jDuqRhMYspPXJZNpMT/view?usp=sharing)  

Use inference_anime_heads module to load these exported models.

## Flask Server and Simple Demo Site

* [Flask Server](server)
* [Demo Site](https://github.com/cwza/deep_t2i_web)

## How to Develop

* Clone this repository
* Run `make install` to install deep_t2i
* Data:
    * Download [CUB-200-2011](http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz) and put it to ./data/full_data/CUB-200-2011.tgz
    * Download [Birds Captions from AttnGAN](https://drive.google.com/open?id=1O_LtUP9sch09QH3s_EBAgLEctBQ5JBSJ)  and put it to ./data/full_data/birds.zip
    * Download [Simple anime faces data](https://drive.google.com/uc?export=download&id=1tpW7ZVNosXsIAWu8-f5EpwtF3ls3pb79) and put it to ./data/full_data/data.zip
    * Run `python3 ./scripts/birds_data.py`
* Make some change in nbs/xxx.ipynb. You can add documentation in notebooks!!!
* Run `make build` to generate code from jupyter notebooks to ./deep_t2i
* Run `make test` to do some unit test
* Run `make build-all` to also generate documentation from notebooks
* Git push


## How to Train

* Clone this repository
* Run `make install` to install deep_t2i
* Data:
    * Download [CUB-200-2011](http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz) and put it to ./data/full_data/CUB-200-2011.tgz
    * Download [Birds Captions from AttnGAN](https://drive.google.com/open?id=1O_LtUP9sch09QH3s_EBAgLEctBQ5JBSJ)  and put it to ./data/full_data/birds.zip
    * Download [Simple anime faces data](https://drive.google.com/uc?export=download&id=1tpW7ZVNosXsIAWu8-f5EpwtF3ls3pb79) and put it to ./data/full_data/data.zip
    * Run `python3 ./scripts/birds_data.py`
* See ./nbs/99c_Train_Birds_DAMSM.ipynb for training DAMSM
* See ./nbs/99d_Train_Birds_GAN.ipynb for training and getting exported model
* See ./nbs/05b_inference_birds.ipynb for inference
