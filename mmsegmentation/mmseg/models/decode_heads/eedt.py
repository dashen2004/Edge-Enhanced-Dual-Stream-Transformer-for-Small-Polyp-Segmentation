import torch
import torch.nn as nn
import torch.nn.functional as F
from mmseg.models.builder import HEADS
from mmseg.models.decode_heads.decode_head import BaseDecodeHead

@HEADS.register_module()
class EEDT(BaseDecodeHead):
    def __init__(self,
                 in_channels,
                 channels=96,
                 heads=8,
                 in_index=[0,1,2,3],
                 image_size=None,
                 input_transform='multiple_select',  
                 **kwargs):
        super().__init__(in_channels=in_channels,
                         channels=channels,
                         in_index=in_index,
                         input_transform=input_transform,
                         **kwargs)
        self.heads = heads

        # -------- Feature Stream projection --------
        self.feature_proj = nn.ModuleList([nn.Conv2d(c, channels, 1) for c in in_channels])

        # -------- Edge Stream: Laplacian-based boundary extraction --------
        self.edge_conv = nn.Conv2d(1, channels, 3, padding=1)
        laplacian_kernel = torch.tensor([[[[0,1,0],[1,-4,1],[0,1,0]]]], dtype=torch.float32)
        self.register_buffer('laplacian_kernel', laplacian_kernel)

        # -------- Cross-Attention --------
        self.cross_attn = nn.MultiheadAttention(embed_dim=channels, num_heads=heads, batch_first=True)
        self.bsr = nn.Identity()

        # -------- Classification convolution --------
        self.cls_conv = nn.Conv2d(channels, self.num_classes, 1)

    def extract_edge(self, x):
        """Laplacian boundary features"""
        edge = F.conv2d(x, self.laplacian_kernel, padding=1)
        edge = F.relu(edge)
        edge = self.edge_conv(edge)
        return edge

    def forward(self, inputs):
        # -------- Feature Stream --------
        feats = [proj(f) for f, proj in zip(inputs, self.feature_proj)]
        H, W = feats[0].shape[2:]
        feats = [F.interpolate(f, size=(H,W), mode='bilinear', align_corners=False) for f in feats]
        feat_map = sum(feats)

        # -------- Edge Stream --------
        gray = feat_map.mean(1, keepdim=True)
        edge_feat = self.extract_edge(gray)

        # -------- Cross-Attention fusion --------
        B, C, H, W = feat_map.shape
        feat_flat = feat_map.flatten(2).transpose(1,2)
        edge_flat = edge_feat.flatten(2).transpose(1,2)
        fused, _ = self.cross_attn(query=feat_flat, key=edge_flat, value=edge_flat)
        fused = fused.transpose(1,2).view(B,C,H,W)

        # -------- Decoder --------
        fused = self.bsr(fused)

        # -------- Classification output --------
        out = self.cls_conv(fused)
        return out
