# DaSiamRPN: Relation Networks for Object Tracking

**Authors:** Wang, Qiang; Zhang, Liangjian; Shen, Cong; Fan, Haibin; Yang, Junjie; and others  
**Venue:** CVPR 2019  

## Core Method
DaSiamRPN (Deep Siamese Region Proposal Network) combines the Siamese tracking architecture with region proposal networks (RPN) for accurate bounding box prediction. The Siamese backbone provides template matching features, while a shared RPN head predicts bounding box refinements. The dual-branch RPN structure handles scale changes and translation simultaneously.

## Key Innovation
First to combine Siamese feature matching with RPN-style bounding box prediction for tracking. The RPN mechanism provides precise bounding box regression that traditional correlation-filter trackers (KCF, CSRT) cannot achieve. This was a major step forward in tracking accuracy.

## Relevance to Blender Motion Tracking
MODERATE relevance. While DaSiamRPN predicts bounding boxes (4 parameter outputs), Blender's motion tracker works with 2D point anchors (2 parameter outputs). However, the Siamese correlation mechanism at the core provides useful matching between frames that could be adapted to point tracking.
