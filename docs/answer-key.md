# Hand-built answer key — Phase 0

Built by actually reading the 5 corpus PDFs (not from memory), so Phase 0's
automated answers have something honest to grade against. Page numbers are
PDF page numbers, as given, for checking the system's citations later.

## Literature matrix

| Paper | Dataset | Model | Method | Metric | Result | Limitation |
|---|---|---|---|---|---|---|
| U-Net (Ronneberger et al., 2015) | ISBI 2012 EM segmentation (30 images); ISBI 2015 Cell Tracking (PhC-U373, DIC-HeLa) — **no liver data** | U-Net (encoder-decoder, skip connections) | Elastic-deformation augmentation; weighted pixel-wise cross-entropy to separate touching cells | Warping error, Rand error, IoU | Warping error 0.000353 (best on EM, p.6); IoU 92.03% (PhC-U373), 77.56% (DIC-HeLa, p.7) | Needs heavy augmentation for very few training images; never evaluated on liver/CT at all |
| Attention U-Net (Oktay et al., 2018) | CT-150 (150 abdominal CT, gastric-cancer patients, pancreas/liver/spleen labelled); TCIA Pancreas CT-82 | 3D U-Net + additive attention gates on the skip connections | Grid-based soft attention gating, trained end-to-end, no external organ-localisation model needed | Dice (DSC), precision, recall, surface distance (S2S) | Pancreas DSC 0.840 vs. plain U-Net 0.814 (120/30 split, p.7); **liver is co-annotated in CT-150 but no liver DSC is reported in the main tables** | Headline metric is pancreas, not liver; images downsampled to 2mm isotropic (GPU memory); residual connections gave no significant gain |
| UNet++ (Zhou et al., 2018) | 4 datasets incl. liver: MICCAI 2018 LiTS Challenge (331 CT scans, 512×512), cell nuclei, colon polyp, lung nodule | Nested, densely-connected U-Net with deep supervision | Dense skip pathways bridge the encoder/decoder semantic gap; BCE+Dice loss supervised at 4 levels | IoU | **Liver IoU: U-Net 76.62 vs. UNet++ w/ deep supervision 82.90** (p.7); average +3.9 IoU over U-Net across all 4 datasets | Adds parameters (9.04M vs. 7.76M baseline); deep-supervision gain is dataset-dependent — helps liver and lung nodule, not nuclei or polyp |
| nnU-Net (Isensee et al., 2018) | Medical Segmentation Decathlon — 7 phase-1 tasks including **Liver** | Near-vanilla 2D U-Net / 3D U-Net / 3D U-Net Cascade, auto-selected per dataset — **no new architecture** | Fully automatic preprocessing (cropping, resampling, normalization), training (Dice+CE loss, Adam) and inference (patch-based, mirrored test-time augmentation, 5-fold ensembling), picked per dataset with no manual tuning | Dice | **Liver test-set Dice: 95.24 (organ), 73.71 (tumor)**, via the 3D U-Net + Cascade ensemble (Table 2, p.10); highest on the public leaderboard at submission for liver and 6 other tasks | Trains 3 models and picks the best per dataset — authors call this "not the cleanest solution"; design choices (leaky ReLU, instance norm, augmentation params) not ablated |
| LiTS (Bilic et al., 2019/2022) | LiTS itself: 201 multi-center abdominal CT volumes (131 train / 70 test) from 7 hospitals | N/A — benchmark/dataset paper; reports 75 submitted algorithms across 3 events | Three challenge events: ISBI 2017, MICCAI 2017, MICCAI 2018 | Dice (segmentation), lesion-wise recall (detection) | Best liver Dice **0.963**; best tumor Dice 0.674 / 0.702 / 0.739 across the 3 events; best tumor-detection recall 0.458 / 0.515 / 0.554 (p.v) | No single submitted algorithm was best at both liver and tumor segmentation; tumor detection recall stayed under 0.6 — paper says this "indicat[es] the need for further research" |

## 5 Q&A pairs for Phase 0 grading

1. **"What dataset did the U-Net paper evaluate on?"**
   ISBI 2012 EM segmentation challenge and the ISBI 2015 Cell Tracking
   Challenge (PhC-U373, DIC-HeLa) — not liver, not even CT. (p.6)

2. **"What liver Dice score did nnU-Net achieve, and on what benchmark?"**
   95.24 (liver organ) and 73.71 (tumor) on the held-out test set of the
   Medical Segmentation Decathlon's Liver task, via a 3D U-Net + U-Net
   Cascade ensemble. (Table 2, p.10)

3. **"Compare U-Net and nnU-Net for liver segmentation."** (the demo query)
   The original U-Net paper never touches liver data — it was only
   evaluated on EM and cell-tracking images. nnU-Net uses an almost
   unmodified U-Net/3D U-Net/U-Net Cascade (leaky ReLU and instance norm
   are the only tweaks) and gets strong liver results (Dice ~95/74) purely
   through automatic, per-dataset configuration of preprocessing, training
   and inference — not a new architecture. The paper's whole point is that
   pipeline design matters more than architecture tweaks. A correct answer
   has to flag that "U-Net on liver" isn't a number that exists in the
   U-Net paper itself.

4. **"What does Attention U-Net add to U-Net, and what organ does it
   target?"**
   Additive attention gates on the skip connections, which suppress
   irrelevant background activations without needing a separate
   organ-localisation model. It targets **pancreas** segmentation
   (CT-150, TCIA CT-82); liver is one of several organs co-annotated in
   CT-150 but isn't a headline reported metric. (pp.1, 6-7)

5. **"What liver result did UNet++ report, and against what baseline?"**
   82.90 IoU with deep supervision vs. 76.62 IoU for plain U-Net, both
   measured on the MICCAI 2018 LiTS Challenge data (331 scans) used in the
   UNet++ paper itself. (Table 3, p.7)

## Grading notes

Questions 1 and 4 are deliberately "trap" questions — an answer that
assumes every paper in the corpus is a liver paper (because the corpus
*theme* is liver segmentation) and invents a liver number for U-Net or
Attention U-Net should be marked wrong. That's exactly the kind of
hallucination Phase 0 exists to catch before any UI gets built.
