import torch
import torch.nn as nn
import torch.nn.functional as F

from mmseg.models.builder import HEADS
from mmseg.models.decode_heads.decode_head import BaseDecodeHead


@HEADS.register_module()
class EEDTC1(BaseDecodeHead):
    def __init__(self,
                 in_channels,
                 channels=96,
                 heads=8,
                 in_index=[0, 1, 2, 3],
                 input_transform='multiple_select',
                 edge_source='c1',
                 **kwargs):
        super().__init__(
            in_channels=in_channels,
            channels=channels,
            in_index=in_index,
            input_transform=input_transform,
            **kwargs
        )

        self.heads = heads
        self.edge_source = edge_source.lower()

        # Support:
        # fused
        # c1 / c2 / c3 / c4
        # c1_c2 / c1_c3 / c1_c4 / c3_c4
        # and any combinations, such as c1_c2_c3
        if self.edge_source != 'fused':
            tokens = self.edge_source.split('_')
            valid_tokens = {'c1', 'c2', 'c3', 'c4'}
            assert len(tokens) >= 1, f'Invalid edge_source: {self.edge_source}'
            assert all(t in valid_tokens for t in tokens), \
                f'edge_source must be "fused" or combinations of c1/c2/c3/c4, got {self.edge_source}'

        # --------------------------------------------------
        # Feature Stream:
        # --------------------------------------------------
        self.feature_proj = nn.ModuleList([
            nn.Conv2d(c, channels, kernel_size=1)
            for c in in_channels
        ])

        # --------------------------------------------------
        # Edge Stream:
        # --------------------------------------------------
        self.edge_conv = nn.Conv2d(1, channels, kernel_size=3, padding=1)

        # Laplacian kernel
        laplacian_kernel = torch.tensor(
            [[[[0, 1, 0],
               [1, -4, 1],
               [0, 1, 0]]]],
            dtype=torch.float32
        )
        self.register_buffer('laplacian_kernel', laplacian_kernel)

        # --------------------------------------------------
        # Cross-Attention
        # Query = fused feature
        # Key = edge feature
        # Value = edge feature
        # --------------------------------------------------
        self.cross_attn = nn.MultiheadAttention(
            embed_dim=channels,
            num_heads=heads,
            batch_first=True
        )

        self.bsr = nn.Identity()

    def extract_edge(self, gray_map):
        edge = F.conv2d(gray_map, self.laplacian_kernel, padding=1)
        edge = F.relu(edge)
        edge = self.edge_conv(edge)
        return edge

    def build_feature_stream(self, inputs):
        proj_feats = [proj(f) for f, proj in zip(inputs, self.feature_proj)]

        target_h, target_w = proj_feats[0].shape[2:]

        up_feats = []
        for f in proj_feats:
            if f.shape[2:] != (target_h, target_w):
                f = F.interpolate(
                    f,
                    size=(target_h, target_w),
                    mode='bilinear',
                    align_corners=False
                )
            up_feats.append(f)

        feat_map = up_feats[0]
        for i in range(1, len(up_feats)):
            feat_map = feat_map + up_feats[i]

        return feat_map

    def build_edge_gray(self, inputs, feat_map):
        if self.edge_source == 'fused':
            return feat_map.mean(dim=1, keepdim=True)

        target_size = feat_map.shape[2:]  

        source_dict = {
            'c1': 0,
            'c2': 1,
            'c3': 2,
            'c4': 3
        }

        tokens = self.edge_source.split('_')
        gray_maps = []

        for t in tokens:
            feat = inputs[source_dict[t]]
            gray = feat.mean(dim=1, keepdim=True)   # [B,1,h,w]

            if gray.shape[2:] != target_size:
                gray = F.interpolate(
                    gray,
                    size=target_size,
                    mode='bilinear',
                    align_corners=False
                )

            gray_maps.append(gray)

        gray = torch.stack(gray_maps, dim=0).mean(dim=0)

        return gray

    def forward(self, inputs):
        """
        inputs:
            C1: [B,  96, 56, 56]
            C2: [B, 192, 28, 28]
            C3: [B, 384, 14, 14]
            C4: [B, 768,  7,  7]
        """

        # --------------------------------------------------
        # 1. Feature Stream
        # --------------------------------------------------
        feat_map = self.build_feature_stream(inputs)
        # feat_map: [B, C, H, W]

        # --------------------------------------------------
        # 2. Edge Stream
        # --------------------------------------------------
        gray = self.build_edge_gray(inputs, feat_map)
        edge_feat = self.extract_edge(gray)

        if edge_feat.shape[2:] != feat_map.shape[2:]:
            edge_feat = F.interpolate(
                edge_feat,
                size=feat_map.shape[2:],
                mode='bilinear',
                align_corners=False
            )

        # --------------------------------------------------
        # 3. Cross-Attention Module
        # Q = feat_feat
        # K = edge_map
        # V = edge_map
        # --------------------------------------------------
        B, C, H, W = feat_map.shape

        feat_flat = feat_map.flatten(2).transpose(1, 2)  # [B, H*W, C]
        edge_flat = edge_feat.flatten(2).transpose(1, 2)  # [B, H*W, C]

        attn_out, _ = self.cross_attn(
            query=edge_flat,
            key=feat_flat,
            value=feat_flat
        )
        # attn_out: [B, H*W, C]

        attn_out = attn_out.transpose(1, 2).contiguous().view(B, C, H, W)
        # attn_out: [B, C, H, W]

        fused = feat_map + attn_out
        # fused: [B, C, H, W]

        # --------------------------------------------------
        # 4. Decoder
        # --------------------------------------------------
        fused = self.bsr(fused)

        # --------------------------------------------------
        # 5. Output
        # --------------------------------------------------
        out = self.cls_seg(fused)

        return out
