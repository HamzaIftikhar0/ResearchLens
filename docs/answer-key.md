# Hand-built answer key — Phase 1A (20-paper corpus)

Built by actually reading all 20 corpus PDFs (not from memory), so the
pipeline's automated answers have something honest to grade against. Page
numbers are PDF page numbers, as given, for checking citations later.

A few of the 15 papers added for Phase 1A were spot-checked twice: read
once in a large parallel batch, then re-read individually to make sure the
batch read hadn't quietly substituted recalled facts for extracted ones.
Every spot-check matched exactly (3D U-Net's 0.863/0.704 IoU, H-DenseUNet's
72.2/82.4/96.1/96.5 leaderboard row, TransUNet's 94.08 liver DSC, the
Cascaded-FCN abstract's "over 94%" claim) — reassuring, but the check was
worth doing before trusting any of it.

## Literature matrix

| Paper | Dataset | Model | Method | Metric | Result | Limitation |
|---|---|---|---|---|---|---|
| U-Net (Ronneberger et al., 2015) | ISBI 2012 EM segmentation (30 images); ISBI 2015 Cell Tracking (PhC-U373, DIC-HeLa) — **no liver data** | U-Net (encoder-decoder, skip connections) | Elastic-deformation augmentation; weighted pixel-wise cross-entropy to separate touching cells | Warping error, Rand error, IoU | Warping error 0.000353 (best on EM, p.6); IoU 92.03% (PhC-U373), 77.56% (DIC-HeLa, p.7) | Needs heavy augmentation for very few training images; never evaluated on liver/CT at all |
| Attention U-Net (Oktay et al., 2018) | CT-150 (150 abdominal CT, gastric-cancer patients, pancreas/liver/spleen labelled); TCIA Pancreas CT-82 | 3D U-Net + additive attention gates on the skip connections | Grid-based soft attention gating, trained end-to-end | Dice (DSC), precision, recall, S2S | Pancreas DSC 0.840 vs. plain U-Net 0.814 (p.7); **liver co-annotated but no liver DSC reported** | Headline metric is pancreas, not liver; 2mm isotropic downsampling (GPU memory) |
| UNet++ (Zhou et al., 2018) | 4 datasets incl. liver: MICCAI 2018 LiTS (331 CT, 512×512), cell nuclei, colon polyp, lung nodule | Nested, densely-connected U-Net with deep supervision | Dense skip pathways bridge encoder/decoder semantic gap; BCE+Dice loss at 4 levels | IoU | **Liver IoU: U-Net 76.62 vs. UNet++ w/ DS 82.90** (p.7) | Adds parameters (9.04M vs. 7.76M); DS gain is dataset-dependent |
| nnU-Net (Isensee et al., 2018) | Medical Segmentation Decathlon — 7 phase-1 tasks incl. **Liver** | Near-vanilla 2D/3D U-Net / U-Net Cascade, auto-selected per dataset | Fully automatic preprocessing, training, inference, picked per dataset | Dice | **Liver test-set Dice: 95.24 (organ), 73.71 (tumor)** (Table 2, p.10) | Trains 3 models, picks the best — "not the cleanest solution" |
| LiTS (Bilic et al., 2019/2022) | LiTS itself: 201 CT volumes (131/70) from 7 hospitals | N/A — benchmark paper; 75 submitted algorithms | 3 challenge events (ISBI 2017, MICCAI 2017/2018) | Dice, lesion-wise recall | Best liver Dice **0.963**; best tumor Dice 0.674→0.702→0.739; best recall 0.554 | No algorithm best at both liver and tumor; tumor recall stayed < 0.6 |
| 3D U-Net (Çiçek et al., 2016) | 3 *Xenopus* kidney volumes, confocal microscopy, sparse 2D-slice annotation — **no liver/CT** | 3D U-Net (extends U-Net to 3D ops, batch norm) | Learns dense 3D segmentation from a few sparsely-annotated 2D slices | IoU | Semi-automated avg IoU **0.863** (3-fold CV, Table 1, p.7); fully-automated avg IoU **0.704** (Table 3, p.7) | Tiny dataset (3 volumes); not CT, not liver, not even human tissue |
| V-Net (Milletari et al., 2016) | PROMISE2012 prostate MRI (50 train / 30 test) — **no liver** | V-Net (volumetric CNN, residual stages, PReLU) | Novel Dice-coefficient loss used directly as the training objective (instead of weighted cross-entropy) | Dice, Hausdorff | Dice 0.869±0.033 (challenge score 82.39); Hausdorff 5.71mm | Prostate-only; never touches liver or CT |
| H-DenseUNet (Li et al., 2018) | LiTS (131/70) + 3DIRCADb (20 volumes, 15 with liver tumors) | 2D DenseUNet-167 + 3D DenseUNet-65, fused via a Hybrid Feature Fusion layer | Auto-context: 2D network's probability maps feed the 3D network, jointly fine-tuned end-to-end | Dice per-case, Dice global | LiTS leaderboard (1 Nov 2017): **lesion 72.2/82.4, liver 96.1/96.5** — ranked 1st on lesion (Table III, p.7); 3DIRCADb liver 98.2%, tumor 93.7% | Small/low-contrast tumors remain the weak point; ~30h training on 2× Titan Xp |
| Cascaded-FCN-liver (Christ et al., 2017) | 100 hepatic-tumor CT volumes (train); 38 MRI liver-tumor volumes + 3DIRCAD (validation) | Two cascaded U-Net-based FCNs (liver ROI → lesion) + 3D dense CRF post-processing | Liver segmented first, crops the ROI, second FCN only segments lesions inside that ROI | Dice | "Dice scores over **94%** for the liver" (abstract, p.1), <100s/volume | Ablation shows a plain U-Net alone only reaches ~53% lesion Dice without the cascade+CRF |
| MSD (Antonelli et al., 2021) | The 10 Decathlon tasks themselves, incl. **Liver** (201 CT) | N/A — reports the challenge, not one model | Development phase (7 known tasks) + mystery phase (3 hidden tasks, no re-tuning allowed) | Dice, Normalised Surface Distance | nnU-Net won both phases; median task DSC ranged **0.16 (colon) to 0.94 (liver)** — liver was the single highest-scoring task in the whole decathlon | Architecture choice (64% of teams used U-Net) mattered less than pipeline design — same conclusion as nnU-Net itself |
| MSD dataset (Simpson et al., 2019) | Describes the same 10 datasets (2,633 images total), incl. Task03_Liver (201 CT, LiTS-derived) | N/A — pure dataset/licensing description | CC-BY-SA 4.0 release, de-identified, reformatted to NIfTI | — | No segmentation results in this paper at all | Companion/earlier paper to MSD (2106.05735) above — don't expect Dice scores here |
| TransUNet (Chen et al., 2021) | Synapse multi-organ CT (30 scans, 8 organs incl. liver); ACDC cardiac MRI | ResNet50+ViT hybrid encoder, CNN-transformer decoder (CUP) with skip connections | Cascaded upsampler reconstructs resolution lost by the transformer encoder | DSC, Hausdorff | Synapse avg DSC 77.48; **Liver DSC 94.08** vs. R50-U-Net's 93.55 (Table 1, p.6) | Pure ViT-only (no CNN) underperforms at 67.86% DSC — hybrid design is load-bearing |
| Swin-Unet (Cao et al., 2021) | Synapse multi-organ CT (18 train/12 test, incl. liver); ACDC | Pure transformer (Swin Transformer blocks, patch merging/expanding, skip connections) | No CNN at all — U-Net-shaped but built entirely from shifted-window self-attention | DSC, Hausdorff | Synapse avg DSC 79.13; **Liver DSC 94.29**; ACDC avg DSC 90.00 | Needs ImageNet-pretrained weights ("severely affected" without); 2D only |
| nnFormer (Zhou et al., 2021) | MSD brain tumor, Synapse multi-organ (incl. liver), ACDC | Interleaved conv + self-attention; "skip attention" instead of concat at skip connections | Local + Global Volume-based Multi-head Self-Attention | DSC, HD95 | Synapse **Liver DSC 96.84**, vs. nnU-Net's 97.23 on the same split (Table V) | On liver specifically, plain nnU-Net edges out nnFormer — gains are elsewhere (pancreas, stomach) |
| UNETR (Hatamizadeh et al., 2021) | BTCV (30 CT, 13 organs incl. liver); MSD brain tumor + spleen | Pure ViT encoder (no CNN backbone) + CNN decoder via skip connections | Transformer processes 3D patches directly; decoder is conventional CNN upsampling | Dice | BTCV **Liver Dice 0.983** (Table 1, bottom/best section) | Training a transformer encoder from scratch (no pretrained weights) "did not demonstrate any performance improvements"; pure-transformer decoder underperforms |
| ResUNet++ (Jha et al., 2019) | Kvasir-SEG (1,000 polyp images) + CVC-612 (612 images) — colonoscopy, **no liver/CT** | ResUNet backbone + squeeze-excitation + ASPP + attention blocks | Stacks 4 architectural add-ons onto a residual U-Net | Dice, mIoU, recall, precision | Kvasir-SEG Dice 0.8133; CVC-612 Dice 0.7955 | More parameters than U-Net/ResUNet → longer training; never touches liver or CT |
| DoubleU-Net (Jha et al., 2020) | 2015 MICCAI polyp detection, CVC-ClinicDB, ISIC-2018 skin lesion, 2018 Data Science Bowl nuclei — **no liver/CT** | Two stacked U-Nets (first with pretrained VGG-19 encoder), ASPP bridge, second U-Net refines input×mask1 | Output of network 1 multiplies the input image, feeding a second full U-Net | DSC, mIoU | Polyp DSC 0.7649 (vs. U-Net's 0.2920); CVC-ClinicDB DSC 0.9239 | More parameters/training time than U-Net; zero liver/CT evaluation |
| SegResNet (Myronenko, 2018) | BraTS 2018 (285 cases, 4 MRI modalities) — **brain tumor, no liver** | Asymmetric encoder-decoder, ResNet blocks (GroupNorm) + VAE regularization branch | VAE branch reconstructs the input image to regularize the shared encoder under limited data | Dice, Hausdorff | Test set (ensemble of 10): Dice ET 0.7664, WT 0.8839, TC 0.8154 — **won BraTS 2018, 1st place** | Brain-only; the VAE branch exists specifically because training data was limited (285 cases) |
| Generalised Dice Loss (Sudre et al., 2017) | BRATS (2D) + an in-house 524-subject white-matter-hyperintensity dataset (3D) — **a loss-function study, not an application paper, no liver** | N/A — evaluates 4 loss functions (WCE, Dice loss, Sensitivity-Specificity, GDL) across 4 existing architectures | Proposes GDLv (volume-weighted Generalized Dice) as a class-imbalance-robust loss | DSC (median, IQR) | GDLv most robust to learning-rate/patch-size choice in both 2D and 3D; **WCE failed to train** in the high-imbalance 3D setting | Tested only on brain pathology; this paper proposes no architecture and reports no liver numbers at all |
| KiTS19 (Heller et al., 2020) | KiTS19: 300 CT scans (210/90), kidney + kidney-tumor labels — **kidney, not liver** | N/A — benchmark paper; 106 teams, winning method = nnU-Net-style 3D U-Net ensemble | Single open/public challenge, Dice-ranked leaderboard | Dice | Winning team: kidney 0.974, tumor 0.851; avg across all 106: kidney 0.915±0.047, **tumor 0.580±0.212** | Same organ-vs-tumor difficulty gap as LiTS, different organ: tumor recall (0.586) lags precision (0.658) — "DNNs often have a difficult time finding the whole tumor" |

## 10 Q&A pairs for grading

1. **"What dataset did the U-Net paper evaluate on?"**
   ISBI 2012 EM segmentation challenge and the ISBI 2015 Cell Tracking
   Challenge (PhC-U373, DIC-HeLa) — not liver, not even CT. (p.6)

2. **"What liver Dice score did nnU-Net achieve, and on what benchmark?"**
   95.24 (liver organ) and 73.71 (tumor) on the held-out test set of the
   Medical Segmentation Decathlon's Liver task. (Table 2, p.10)

3. **"Compare U-Net and nnU-Net for liver segmentation."** (the original
   demo query)
   The original U-Net paper never touches liver data — EM and cell-tracking
   only. nnU-Net uses an almost unmodified U-Net/3D U-Net/U-Net Cascade and
   gets strong liver results (Dice ~95/74) purely through automatic,
   per-dataset configuration — not a new architecture. A correct answer has
   to flag that "U-Net on liver" isn't a number the U-Net paper itself reports.

4. **"What does Attention U-Net add to U-Net, and what organ does it
   target?"**
   Additive attention gates on the skip connections. It targets
   **pancreas** segmentation; liver is co-annotated in CT-150 but isn't a
   headline reported metric. (pp.1, 6-7)

5. **"What liver result did UNet++ report, and against what baseline?"**
   82.90 IoU with deep supervision vs. 76.62 IoU for plain U-Net, both on
   the MICCAI 2018 LiTS Challenge data. (Table 3, p.7)

6. **"Which papers in this corpus report no liver segmentation result at
   all?"** (aggregate trap question, only answerable at 20-paper scale)
   Nine: U-Net, Attention U-Net, 3D U-Net, V-Net, ResUNet++, DoubleU-Net,
   SegResNet, the Generalised Dice Loss paper, and KiTS19. A correct answer
   should list roughly this set and not silently invent a liver number for
   any of them just because the corpus theme is liver segmentation.

7. **"Compare CNN-based and transformer-based architectures on liver
   segmentation specifically."**
   On their respective organ-segmentation splits: TransUNet 94.08
   (Synapse), Swin-Unet 94.29 (Synapse), nnFormer 96.84 (Synapse),
   UNETR 0.983 (BTCV — a different split, not directly comparable).
   Transformer-hybrid gains over CNN baselines (e.g. R50-U-Net's 93.55 on
   Synapse) are real but modest on liver specifically — a correct answer
   should note liver is already a comparatively "easy," high-Dice organ
   across *all* methods, so the biggest transformer-vs-CNN gaps in these
   papers show up on harder organs (pancreas, stomach, gallbladder), not liver.
   Splits differ between papers (Synapse vs. BTCV vs. Decathlon), so a
   precise answer should not present these as one ranked leaderboard.

8. **"How does H-DenseUNet relate to the Cascaded-FCN-liver paper?"**
   Both target liver+tumor segmentation on overlapping data (LiTS /
   3DIRCADb). Cascaded-FCN (2017) is two separate cascaded plain U-Nets
   plus a 3D CRF post-processing step. H-DenseUNet (2018) replaces that
   with a single jointly-trained hybrid 2D+3D DenseUNet and improves
   specifically on lesion segmentation (ranked 1st on the LiTS leaderboard
   lesion score at submission) — showing the field's progression from
   "cascade + CRF" toward end-to-end joint 2D/3D feature fusion.

9. **"What does the Generalised Dice Loss paper contribute, and does it
   report a liver result?"** (method-paper trap)
   No liver result — it's a loss-function study, not a segmentation
   architecture or application paper. It evaluates 4 loss functions across
   4 existing architectures on brain tumor and white-matter-hyperintensity
   data, and proposes GDLv as more robust to class imbalance and
   hyperparameter choice than weighted cross-entropy. Several other corpus
   papers (nnU-Net, SegResNet) use a Dice-based loss directly relevant to
   this paper's findings, but neither applies GDLv specifically.

10. **"Across LiTS, the Decathlon, and KiTS19, how does organ segmentation
    difficulty compare to tumor segmentation difficulty?"**
    Consistently, organ segmentation is far more solved than tumor/lesion
    segmentation: LiTS best liver Dice 0.963 vs. best tumor Dice 0.739;
    Decathlon liver was the single highest-scoring task (median DSC 0.94)
    of all ten; KiTS19 winning kidney Dice 0.974 vs. tumor Dice 0.851, and
    the average submission scored kidney 0.915 vs. tumor only 0.580. The
    same organ-vs-tumor gap recurs across three independent benchmarks and
    two organs (liver, kidney) — a correct answer should name this as a
    cross-benchmark pattern, not something specific to LiTS alone.

## Grading notes

Questions 1, 4, and 6 are deliberately "trap" questions — an answer that
assumes every paper in the corpus is a liver paper (because the corpus
*theme* is liver segmentation) and invents a liver number for a paper that
doesn't report one should be marked wrong. Question 9 is the same trap
applied to a *method* paper (a loss function, not an architecture).
Questions 7, 8, and 10 require synthesizing across multiple papers and are
only answerable now that the corpus is 20 papers rather than 5 — that's the
actual point of Phase 1A.
