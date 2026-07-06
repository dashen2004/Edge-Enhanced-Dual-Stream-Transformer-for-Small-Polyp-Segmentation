# <p align=center>`Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation`</p>

> **Authors:**
> [Youyao Gao](), [Ziqian Xiong](), [Yiwei Li](), [Hengyuan Shi](), & [Fiseha Berhanu Tesema]().


This document mainly contains [Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation]()'s training, testing and other experimental methods, experimental results and visualization results, etc.

## **Abstract**

We present EEDT, an edge-enhanced dual-stream Transformer framework for small polyp segmentation. 
Small polyps in colonoscopy images often suffer from low contrast, blurred boundaries, and complex backgrounds, making accurate segmentation difficult when relying only on semantic features. 
To address this issue, EEDT introduces an auxiliary edge-enhancement stream to explicitly strengthen boundary cues while preserving the semantic representation learned by the main feature stream. Specifically, a Swin Transformer encoder extracts multi-level features, which are then processed by a semantic feature stream and an edge-enhancement stream. 
A cross-attention fusion module is further designed to integrate semantic features with boundary-aware information for more accurate polyp delineation.
Experiments on five public polyp segmentation datasets demonstrate that EEDT achieves competitive performance compared with representative CNN-based, Transformer-based, and refinement-based methods. 
Additional small-polyp experiments and ablation studies further validate the effectiveness of the proposed edge-enhancement stream and cross-attention fusion module.

## Architecture

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


## Experiments

### Dataset

- 1.Download the dataset mentioned in the initial [README.md](https://github.com/dashen2004/Edge-Enhanced-Dual-Stream-Transformer-for-Small-Polyp-Segmentation/blob/main/README.md##L25-L60), then decompress the dataset.
- 2.Update the training path and test path of **/medical_seg/mmsegmentation/local_config/_base_/datasets/polypseg.py** in the project, on lines 55, 56, 67, and 68 respectively.
> We recommend using absolute paths instead of relative paths when updating paths of dataset.
- 3.Create a folder in the root directory

Creat Training Dataset
```
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/image/
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/mask/
```

Creat Testing Dataset
```
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/Kvasir/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/Kvasir/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-300/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-300/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ClinicDB/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ClinicDB/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ColonDB/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ColonDB/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/ETIS-LaribPolypDB/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/ETIS-LaribPolypDB/mask
```

Creat Small Polyp Testing Dataset
```
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/Kvasir/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/Kvasir/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-300/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-300/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ClinicDB/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ClinicDB/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ColonDB/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ColonDB/mask

sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/ETIS-LaribPolypDB/images
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/ETIS-LaribPolypDB/mask
```

- 4.Copy the database to the root directory

Copy Training Dataset
```
sudo cp -r /home/ubuntu/Desktop/TrainDataset/TrainDataset/image/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/image/
sudo cp -r /home/ubuntu/Desktop/TrainDataset/TrainDataset/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/mask/
```

Copy Testing Dataset
```
sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/Kvasir/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/Kvasir/images/
sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/Kvasir/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/Kvasir/mask/

sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/CVC-300/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-300/images/
sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/CVC-300/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-300/mask/

sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/CVC-ClinicDB/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ClinicDB/images/
sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/CVC-ClinicDB/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ClinicDB/mask/

sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/CVC-ColonDB/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ColonDB/images/
sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/CVC-ColonDB/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/CVC-ColonDB/mask/

sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/ETIS-LaribPolypDB/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/ETIS-LaribPolypDB/images/
sudo cp -r /home/ubuntu/Desktop/TestDataset/TestDataset/ETIS-LaribPolypDB/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/TestDataset/ETIS-LaribPolypDB/mask/
```

Copy Small Polyp Testing Dataset
```
sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/Kvasir/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/Kvasir/images/
sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/Kvasir/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/Kvasir/mask/

sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/CVC-300/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-300/images/
sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/CVC-300/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-300/mask/

sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/CVC-ClinicDB/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ClinicDB/images/
sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/CVC-ClinicDB/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ClinicDB/mask/

sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/CVC-ColonDB/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ColonDB/images/
sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/CVC-ColonDB/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/CVC-ColonDB/mask/

sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/ETIS-LaribPolypDB/images/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/ETIS-LaribPolypDB/images/
sudo cp -r /home/ubuntu/Desktop/SmallPolypDataset/ETIS-LaribPolypDB/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TestDataset/SmallPolypDataset/ETIS-LaribPolypDB/mask/
```

### Training
Please confirm whether you are currently under the mmsegmentation directory. If not, please enter the mmsegmentation directory. Then run the following code in terminal:

```
python tools/train.py local_config/EEDT/main/eedt_polypseg_224*224_80k.py
```

> During training, verification is performed every 8,000 iterations, and the checkpoint file is saved at the same time.

> The batch size and validation set evaluation indicators can be changed in **/medical_seg/mmsegmentation/local_config/EEDT/main/eedt_polypseg_224*224_80k**.

For the EEDT_c1 model, run the following code in terminal:

```
python tools/train.py local_config/EEDT_c1/main/eedt_c1_polypseg_224*224_80k.py
```

### Testing

The log files and checkpoint files of the training process are saved in /medical_seg/mmsegmentation/work_dirs/eedt_polypseg_224*224_80k/. The command to test the model is as follows:

```
python tools/test.py local_config/EEDT/main/eedt_polypseg_224*224_80k.py work_dirs/eedt_polypseg_224*224_80k/iter_80000.pth
```

> You can replace iter_80000.pth to evaluate the performance of different checkpoints. 

> The evaluation indicators supported by mmsegmentation can be found in **/medical_seg/mmsegmentation/mmseg/evaluation/metrics**.\

> You can chaneg the testing dataset in **/medical_seg/mmsegmentation/local_config/_base_/datasets/polypseg.py**

For the EEDT_c1 model, run the following code in terminal:

```
python tools/test.py local_config/EEDT_c1/main/eedt_c1_polypseg_224*224_80k.py work_dirs/eedt_c1_polypseg_224*224_80k/iter_80000.pth
```

### Ablation Study

If you want to perform ablation experiments, we recommend that you do so as follows:

- 1.Create a new file in the /mmsegmentation/mmseg/models/decode_heads directory, for example, name it ablation.py. The ablation experiment can be modified by referring to /mmsegmentation/mmseg/models/decode_heads/eedt.py. For example, you can change ablation.py The function inside is named "Ablationhead".

- 2.Add your newly created function name "Ablationhead" to the __init__.py file in the /mmsegmentation/mmseg/models/decode_heads directory. You can refer to polyper to add it.

- 3.After the addition is completed, run **python setup.py install** in the command windows.

- 4.Create a new python file in the /mmsegmentation/local_config/EEDT/main folder. You can use the settings of /mmsegmentation/local_config/EEDT/main/eedt_polypseg_224*224_80k and replace the type parameter of decode_head. into your new head, such as "Ablationhead".

> You can also refer to [mmsegmentation](https://mmsegmentation.readthedocs.io/zh-cn/latest/) of "自定义组件/新增模块" to make changes. We implement it based on mmsegmentation. It is recommended that you read [mmsegmentation](https://mmsegmentation.readthedocs.io/zh-cn/latest/) for a better understanding.
