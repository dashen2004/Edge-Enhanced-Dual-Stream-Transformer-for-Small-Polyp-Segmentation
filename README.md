# <p align=center>`Edge-Enhanced Dual Stream Transformer for Small Polyp Segementation`</p>

<p align="center">
📃 <b>Contents:</b>
<a href="#highlights">🌤️Highlights</a> |
<a href="#getstart">✅Get Start</a> |
<a href="#ourwork">📖Our Work</a>
</p>

<p align="center">
✍
  <b>Authors:</b> 
  <a href="https://github.com/dashen2004">Youyao Gao</a>, 
  <a href="https://github.com/qianqqqqqXZQ">Ziqian Xiong</a>, 
  <a href="https://github.com/daidaibunny">Yiwei Li</a>, 
  <a href="">Hengyuan Shi</a>, 
  <a href="">Name</a>, 
  <a href="https://github.com/Falmi">Fiseha Berhanu Tesema</a>
</p>

:fire::fire: This is an official repository of our work on edge enhanced dual stream transformer for small polyp segementation. :fire::fire:

> ✉If you have any questions about our work, feel free to contact me via e-mail (📫youyaog@andrew.cmu.edu / youyaogao@gmail.com).

<a id="highlights"></a>

## 🌤️ Highlights
- (2025.02.18) The Jittor vsersion implementation of  [Polyper: Boundary Sensitive Polyp Segmentation](https://ojs.aaai.org/index.php/AAAI/article/view/28274) is available at [Jittor Version](https://github.com/haoshao-nku/medical_seg_jittor.git) !!!

<a id="getstart"></a>

## ✅ Get Start
> Our experiments are based on ubuntu, and windows is not recommended.
> 
**0. Install**

```
conda create --name medical_seg python=3.8 -y
conda activate medical_seg
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"

cd mmsegmentation
pip install -v -e .
pip install ftfy
pip install regex
pip install einops
```

The following methods can be used to verify that the experimental environment is successfully set up:
```
1. mim download mmsegmentation --config pspnet_r50-d8_4xb2-40k_cityscapes-512x1024 --dest .
2. python demo/image_demo.py demo/demo.png configs/pspnet/pspnet_r50-d8_4xb2-40k_cityscapes-512x1024.py pspnet_r50-d8_512x1024_40k_cityscapes_20200605_003338-2966598c.pth --device cuda:0 --out-file result.jpg
```
After the preceding two steps are successfully run, if the result.png file is generated under the mmsegmentation folder, the environment is successfully created.The result.png as shown in the following.

<p align="center"><img width="800" alt="image" src="https://github.com/haoshao-nku/medical_seg/blob/master/mmsegmentation/demo/result.jpg"></p> 

**1. Dataset**
> The dataset used in the experiment can be obtained in the following methods:
- For polyp segmentation task: [Polypseg](https://github.com/DengPingFan/PraNet): including Kvasir, - CVC-ClinicDB, CVC-ColonDB, EndoScene and ETIS dataset.
- For abdominal multi-organ segmentation task: [Synapse](https://github.com/Beckschen/TransUNet).
- For skin lesion segmentation task: [ISIC-2018](https://challenge.isic-archive.com/data/#2018).
- For nuclei segmentation task: [DSB2018](https://www.kaggle.com/c/data-science-bowl-2018).

**2. Experiments**
We recommend that you place the project folder in a location such as a solid state drive, and put the checkpoint files generated from the experiment on a mechanical hard drive to save space, so you can choose to create a soft connection. Specific practices are as follows:

> ln -s   "mechanical hard disk path"  /medical_seg/mmsegmentation/work_dirs

If your hardware resources are relatively rich, ignore this advice.

> **Note: Our experiment is implemented based on [mmsegmentation](https://github.com/open-mmlab/mmsegmentation). The environment configuration can also refer to the [mmsegmentation](https://github.com/open-mmlab/mmsegmentation), and questions about the entire project can refer to the [official documentation](https://mmsegmentation.readthedocs.io/zh-cn/latest/).**

<a id="ourwork"></a>

## 📖 Our Work

### [Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation]() 2026

> **Authors:**
> [Youyao Gao](), [Ziqian Xiong](), [Yiwei Li](), [Hengyuan Shi](), [Name](), &[Fiseha Berhanu Tesema]().

#### **Abstract**

This paper presents an edge-enhanced dual-stream Transformer framework for small polyp segmentation, named EEDT. The proposed method is motivated by a key challenge in small polyp segmentation: in colonoscopy images, small polyps often suffer from low contrast, blurred boundaries, irregular shapes, and complex background interference. Therefore, relying only on conventional semantic features may not be sufficient to produce accurate boundary predictions. To address this problem, EEDT explicitly introduces edge-enhanced information to improve the model's discrimination capability around polyp boundaries while maintaining relatively low computational cost. Specifically, a Swin Transformer is first adopted as the encoder to extract multi-level semantic features. Then, an edge-enhancement stream is designed to capture boundary-related responses from feature maps through channel averaging, Laplacian convolution, and feature projection. After that, a cross-attention fusion module is introduced to promote effective interaction between semantic features and edge-enhanced features. In this way, the model can preserve the main regional semantic information while enhancing its ability to model fine-grained boundary structures. To evaluate the effectiveness of the proposed method, experiments are conducted on five public polyp segmentation datasets, including Kvasir-SEG, CVC-ClinicDB, CVC-ColonDB, EndoScene, and ETIS-LaribPolypDB. The experimental results show that EEDT achieves competitive segmentation performance across multiple datasets. Further ablation studies also demonstrate that both the edge-enhancement stream and the cross-attention module improve model performance, and their combination achieves the best results.

#### Architecture

<p align="center">
    <img src="https://github.com/dashen2004/Edge-Enhanced-Dual-Stream-Transformer-for-Small-Polyp-Segmentation/blob/main/fig/eedt.png"/> <br />
    <em> 
    Figure 1: Overall architecture of the proposed Edge-Enhanced Dual-Stream Transformer (EEDT).
    </em>
</p>


<p align="center">
    <img src="https://github.com/dashen2004/Edge-Enhanced-Dual-Stream-Transformer-for-Small-Polyp-Segmentation/blob/main/fig/feature_map.png"/> <br />
    <em> 
    Figure 2: Architecture of the feature stream.
    </em>
</p>

<p align="center">
    <img src="https://github.com/dashen2004/Edge-Enhanced-Dual-Stream-Transformer-for-Small-Polyp-Segmentation/blob/main/fig/edge_feat_map.png"/> <br />
    <em> 
    Figure 3: Architecture of the edge-enhanced stream.
    </em>
</p>

<p align="center">
    <img src="https://github.com/dashen2004/Edge-Enhanced-Dual-Stream-Transformer-for-Small-Polyp-Segmentation/blob/main/fig/QKV.png"/> <br />
    <em> 
    Figure 4: Architecture of the attention fusion module.
    </em>
</p>


#### Experiments

> For training, testing and other details can be found at **/medical_seg/mmsegmentation/local_config/Polyper-AAAI2024/readme.md**.



## ❤ Acknowlegement

Thanks [mmsegmentation](https://github.com/open-mmlab/mmsegmentation) providing a friendly codebase for segmentation tasks. And our code is built based on it.

## 🖊 Reference
You may want to cite:
```
@inproceedings{shao2024polyper,
  title={Polyper: Boundary Sensitive Polyp Segmentation},
  author={Shao, Hao and Zhang, Yang and Hou, Qibin},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={38},
  number={5},
  pages={4731--4739},
  year={2024}
}

@article{shao2023mcanet,
  title={MCANet: Medical Image Segmentation with Multi-Scale Cross-Axis Attention},
  author={Shao, Hao and Zeng, Quansheng and Hou, Qibin and Yang, Jufeng},
  journal={arXiv preprint arXiv:2312.08866},
  year={2023}
}
```




### License

Code in this repo is for non-commercial use only.
