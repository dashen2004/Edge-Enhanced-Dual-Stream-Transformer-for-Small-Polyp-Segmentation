# <p align=center>`Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation`</p>

> **Authors:**
> [Hao Shao](https://scholar.google.com/citations?hl=en&user=vB4DPYgAAAAJ), [Yang Zhang](), &[Qibin Hou](https://scholar.google.com/citations?user=fF8OFV8AAAAJ&hl=en&oi=ao).



This document mainly contains [Edge-Enhanced Dual-Stream Transformer for Small Polyp Segmentation](https://arxiv.org/abs/2312.08735)'s training, testing and other experimental methods, experimental results and visualization results, etc.

## **Abstract**

We present a new boundary sensitive framework for polyp segmentation, called Polyper. Our method is motivated by a clinical approach that seasoned medical practitioners often leverage the inherent features of interior polyp regions to tackle blurred boundaries. Inspired by this, we propose explicitly leveraging polyp regions to bolster the model’s boundary discrimination capability while minimizing computation. Our approach first extracts boundary and polyp regions from the initial segmentation map through morphological operators. Then, we design the boundary sensitive attention that concentrates on augmenting the features near the boundary regions using the interior polyp regions’s characteristics to generate good segmentation results. Our proposed method can be seamlessly integrated with classical encoder networks, like ResNet-50, MiT-B1, and Swin Transformer. To evaluate the effectiveness of Polyper, we conduct experiments on five publicly available challenging datasets, and receive state-of-the-art performance on all of them.

## Architecture

<p align="center">
    <img src="https://github.com/haoshao-nku/medical_seg/blob/master/fig/pipline_polyper.png"/> <br />
    <em> 
    Figure 1: Overall architecture of Polyper. We use the Swin-T from Swin Transformer as the encoder. The decoder is divided into two main stages. The first potential boundary extraction (PBE) stage aims to capture multi-scale features from the encoder, which are then aggregated to generate the initial segmentation results. Next, we extract the predicted polyps' potential boundary and interior regions using morphology operators. In the second boundary sensitive refinement (BSR) stage, we model the relationships between the potential boundary and interior regions to generate better segmentation results.
    </em>
</p>


<p align="center">
    <img src="https://github.com/haoshao-nku/medical_seg/blob/master/fig/refine_polyper.png"/> <br />
    <em> 
    Figure 2: Detailed structure of boundary sensitive attention (BSA) module. This process is separated into two parallel branches, which systematically capitalize on the distinctive attributes of polyps at various growth stages, both in terms of spatial and channel characteristics. `B' and `M' indicate the number of pixels in the boundary and interior polyp regions within an input of size H*W and C channels.
    </em>
</p>

## Experiments

### Dataset

- 1.Download the [Polypseg](https://github.com/DengPingFan/PraNet) dataset, then decompress the dataset.
- 2.Update the training path and test path of **/medical_seg/mmsegmentation/local_config/_base_/datasets/polypseg.py** in the project, on lines 55, 56, 67, and 68 respectively.
> We recommend using absolute paths instead of relative paths when updating paths of dataset.
- 3.Create a folder in the root directory

```
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/image/
sudo mkdir -p /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/mask/

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

- 4.Copy the database to the root directory

```
sudo cp -r /home/ubuntu/Desktop/TrainDataset/TrainDataset/image/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/image/
sudo cp -r /home/ubuntu/Desktop/TrainDataset/TrainDataset/masks/* /data/dataset/medical_image_segmentation/Polyp_Segmentation/TrainDataset/mask/

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

### Training
Please confirm whether you are currently under the mmsegmentation directory. If not, please enter the mmsegmentation directory. Then run the following code in terminal:

```
python tools/train.py local_config/EEDT/main/eedt_polypseg_224*224_80k.py
```

> During training, verification is performed every 8,000 iterations, and the checkpoint file is saved at the same time. The batch size and validation set evaluation indicators can be changed in **/medical_seg/mmsegmentation/local_config/EEDT/main/eedt_polypseg_224*224_80k**.

### Testing

The log files and checkpoint files of the training process are saved in /medical_seg/mmsegmentation/work_dirs/eedt_polypseg_224*224_80k/. The command to test the model is as follows:

```
python tools/test.py local_config/EEDT/main/eedt_polypseg_224*224_80k.py work_dirs/eedt_polypseg_224*224_80k/iter_80000.pth
```

>  You can replace iter_80000.pth to evaluate the performance of different checkpoints. 

> The evaluation indicators supported by mmsegmentation can be found in **/medical_seg/mmsegmentation/mmseg/evaluation/metrics**.

### Ablation Study

If you want to perform ablation experiments, we recommend that you do so as follows:

- 1.Create a new file in the /mmsegmentation/mmseg/models/decode_heads directory, for example, name it ablation.py. The ablation experiment can be modified by referring to /mmsegmentation/mmseg/models/decode_heads/eedt.py. For example, you can change ablation.py The function inside is named "Ablationhead".

- 2.Add your newly created function name "Ablationhead" to the __init__.py file in the /mmsegmentation/mmseg/models/decode_heads directory. You can refer to polyper to add it.

- 3.After the addition is completed, run **python setup.py install** in the command windows.

- 4.Create a new python file in the /mmsegmentation/local_config/EEDT/main folder. You can use the settings of /mmsegmentation/local_config/EEDT/main/eedt_polypseg_224*224_80k and replace the type parameter of decode_head. into your new head, such as "Ablationhead".

> You can also refer to [mmsegmentation](https://mmsegmentation.readthedocs.io/zh-cn/latest/) of "自定义组件/新增模块" to make changes. We implement it based on mmsegmentation. It is recommended that you read [mmsegmentation](https://mmsegmentation.readthedocs.io/zh-cn/latest/) for a better understanding.
