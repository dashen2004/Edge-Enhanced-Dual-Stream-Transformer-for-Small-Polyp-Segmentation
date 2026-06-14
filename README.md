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
- (2026.06.14) The Initial vsersion of [Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation](https://ojs.aaai.org/index.php/AAAI/article/view/28274) is available.

## ✅ Get Start
> Our experiments are based on ubuntu, and windows is not recommended.

**0. Install**

```
conda create --name medical_seg python=3.10 -y
conda activate medical_seg
conda install pytorch torchvision torchaudio pytorch-cuda=12.8 -c pytorch -c nvidia
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"

cd mmsegmentation
pip install -v -e .
pip install ftfy
pip install regex
pip install einops
```
If you encounter the error: AssertionError: **MMCV==2.2.0** is used but incompatible. Please install **mmcv>=2.0.0rc4**, modify the **mmsegmentation/mmseg/__init__.py file**.

The following methods can be used to verify that the experimental environment is successfully set up:

```
mim download mmsegmentation --config pspnet_r50-d8_4xb2-40k_cityscapes-512x1024 --dest .
```

```
python demo/image_demo.py demo/demo.png configs/pspnet/pspnet_r50-d8_4xb2-40k_cityscapes-512x1024.py pspnet_r50-d8_512x1024_40k_cityscapes_20200605_003338-2966598c.pth --device cuda:0 --out-file result.jpg
python demo/image_demo.py demo/demo.png configs/pspnet/pspnet_r50-d8_4xb2-40k_cityscapes-512x1024.py pspnet_r50-d8_512x1024_40k_cityscapes_20200605_003338-2966598c.pth --device cpu --out-file result.jpg
```
After the preceding two steps are successfully run, if the result.png file is generated under the mmsegmentation folder, the environment is successfully created.The result.png as shown in the following.

<p align="center"><img width="800" alt="image" src="https://github.com/haoshao-nku/medical_seg/blob/master/mmsegmentation/demo/result.jpg"></p> 


To check whether the GPU has properly installed PyTorch and the corresponding CUDA version, and whether it is available for computation, you can use the following command for a quick test:
```
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available())"
```

**1. Dataset**
> The dataset used in the experiment can be obtained in the following methods:
- [Polypseg](https://github.com/DengPingFan/PraNet): including Kvasir, - CVC-ClinicDB, CVC-ColonDB, EndoScene and ETIS dataset.
-

**2. Experiments**

We recommend that you place the project folder in a location such as a solid state drive, and put the checkpoint files generated from the experiment on a mechanical hard drive to save space, so you can choose to create a soft connection. Specific practices are as follows:

> ln -s   "mechanical hard disk path"  /medical_seg/mmsegmentation/work_dirs

If your hardware resources are relatively rich, ignore this advice.

> **Note: Our experiment is implemented based on [mmsegmentation](https://github.com/open-mmlab/mmsegmentation). The environment configuration can also refer to the [mmsegmentation](https://github.com/open-mmlab/mmsegmentation), and questions about the entire project can refer to the [official documentation](https://mmsegmentation.readthedocs.io/zh-cn/latest/).**

<a id="ourwork"></a>

> For training, testing and other details can be found at **/medical_seg/mmsegmentation/local_config/readme.md**.

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

## ❤ Acknowlegement

Thanks [mmsegmentation](https://github.com/open-mmlab/mmsegmentation) providing a friendly codebase for segmentation tasks. And our code is built based on it.

## 🖊 Reference
You may want to cite:
```
@inproceedings{shao2024polyper,
  title={Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation},
  author={},
  booktitle={},
  volume={},
  number={},
  pages={},
  year={2026}
}
```

### License

Code in this repo is for non-commercial use only.
