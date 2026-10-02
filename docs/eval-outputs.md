# Eval run output (ungraded)

## Q1. What dataset did the U-Net paper evaluate on?

Based on the provided excerpts, the U-Net paper evaluated on the following datasets across three segmentation tasks:

1. **EM Segmentation Challenge dataset (ISBI 2012):** Used for the segmentation of neuronal structures in electron microscopic recordings. The training data consists of 30 images ($512 \times 512$ pixels) obtained from serial section transmission electron microscopy of the *Drosophila* first instar larva ventral nerve cord (VNC) [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 6].
2. **"PhC-U373" dataset (ISBI Cell Tracking Challenge 2014 and 2015):** Contains Glioblastoma-astrocytoma U373 cells on a polyacrylamide substrate recorded by phase contrast microscopy, consisting of 35 partially annotated training images [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 7].
3. **"DIC-HeLa" dataset (ISBI Cell Tracking Challenge 2014 and 2015):** Contains HeLa cells on a flat glass recorded by differential interference contrast (DIC) microscopy, consisting of 20 partially annotated training images [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 7].

**Retrieved from:**
- [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 1]
- [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 7]
- [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 4]
- [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 6]
- [3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation, page 1]
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 1]
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 5]
- [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 2]

## Q2. What liver Dice score did nnU-Net achieve, and on what benchmark?

Based on the provided excerpts, nnU-Net was evaluated on the **Medical Segmentation Decathlon** benchmark [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 1, 9; The Medical Segmentation Decathlon, page 33]. Its reported liver Dice scores include:

* **Held-out test set (Phase 1):** nnU-Net achieved a test set Dice score of **95.24** for liver (label 1) and **73.71** for label 2 [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].
* **Five-fold cross-validation (Phase 1):** For liver (label 1), the models achieved mean Dice scores of:
  * 2D U-Net: **94.37** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
  * 3D U-Net: **94.11** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
  * 3D U-Net stage 1 only (U-Net Cascade): **94.69** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
  * 3D U-Net (U-Net Cascade): **95.38** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
  * Ensemble (2D U-Net + 3D U-Net): **94.30** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
  * Ensemble (2D U-Net + 3D U-Net Cascade): **95.31** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
  * Ensemble (3D U-Net + 3D U-Net Cascade): **95.43** [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
* **Medical Segmentation Decathlon development phase summary table:** nnU-Net is reported with a mean Dice Similarity Coefficient of **0.93** for Liver (and **0.74** for Cancer) [The Medical Segmentation Decathlon, page 33].

**Retrieved from:**
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 1]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 3]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 1]
- [The Medical Segmentation Decathlon, page 33]
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 2]
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 8]

## Q3. Compare U-Net and nnU-Net for liver segmentation.

Based on the provided excerpts, the comparison between standard U-Net models and nnU-Net for liver segmentation includes the following aspects:

### 1. Framework and Methodology
* **Standard U-Net:** The U-Net was introduced in 2015 as a medical segmentation benchmark, but adapting it to new tasks involves numerous degrees of freedom (network architecture, preprocessing, training, and inference) that are often modified with specialized tweaks [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 1]. For example, earlier standalone implementations of U-Net yielded a Dice score of 72.9% on the 3DIRCAD liver dataset [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 13].
* **nnU-Net:** Instead of adding architectural modifications, nnU-Net is a self-adapting framework based on 2D and 3D vanilla U-Nets [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 1]. It fully automates adaptive preprocessing, training schemes, and inference [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]. For each task, it runs five-fold cross-validation on three automatically configured U-Net models (2D U-Net, 3D U-Net, and U-Net Cascade) and selects the best model or ensemble based on foreground Dice score [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].

### 2. Liver Segmentation Performance
In the Medical Segmentation Decathlon challenge, nnU-Net evaluated several U-Net configurations on the Liver dataset (label 1 = liver, label 2 = lesion/tumor) [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]:
* **2D U-Net:** Achieved cross-validation mean Dice scores of 94.37% (label 1) and 53.94% (label 2) [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].
* **3D U-Net:** Achieved cross-validation mean Dice scores of 94.11% (label 1) and 61.74% (label 2) [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].
* **3D U-Net Cascade:** Achieved cross-validation mean Dice scores of 95.38% (label 1) and 58.49% (label 2) (and 94.69% / 47.01% for stage 1 only) [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].
* **Ensembles:** Combining models yielded higher scores; for instance, the ensemble of 3D U-Net + 3D U-Net Cascade achieved 95.43% for label 1 and 61.82% for label 2 [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].
* **Final Submissions / Test Results:** 
  * On the held-out test set, nnU-Net reached a Dice score of 95.24% for label 1 and 73.71% for label 2 [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].
  * In the Medical Segmentation Decathlon development phase table, nnU-Net is recorded with a mean Dice Similarity Coefficient of 0.93 for liver and 0.74 for cancer [The Medical Segmentation Decathlon, page 33].

### 3. Model Preference for the Liver Task
* While nnU-Net's general tendency across tasks favors the U-Net Cascade (or 3D U-Net if a cascade cannot be applied), the authors specifically note that the Liver task (along with Prostate) is a close exception to this preference [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].

**Retrieved from:**
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 1]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 13]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 29]
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 1]
- [The Medical Segmentation Decathlon, page 33]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 3]

## Q4. What does Attention U-Net add to U-Net, and what organ does it target?

Based on the excerpts:

* **What it adds to U-Net:** Attention U-Net incorporates novel **attention gates (AGs)** into the standard U-Net architecture [Attention U-Net: Learning Where to Look for the Pancreas, page 1, page 5]. These gates filter the features passed through the skip connections, using contextual information from coarser scales to suppress irrelevant and noisy background activations while highlighting salient foreground features useful for the task [Attention U-Net: Learning Where to Look for the Pancreas, page 1, page 4, page 5].
* **What organ it targets:** It specifically targets the **pancreas** (for CT pancreas segmentation) [Attention U-Net: Learning Where to Look for the Pancreas, page 1, page 2], while also being evaluated on multi-class abdominal segmentation that includes organs such as the spleen and kidney [Attention U-Net: Learning Where to Look for the Pancreas, page 6, page 7].

**Retrieved from:**
- [Attention U-Net: Learning Where to Look for the Pancreas, page 1]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 5]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 7]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 4]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 2]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 8]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 3]
- [Attention U-Net: Learning Where to Look for the Pancreas, page 6]

## Q5. What liver result did UNet++ report, and against what baseline?

Based on the provided excerpts, UNet++ evaluated liver segmentation on CT images from the MICCAI 2018 LiTS Challenge [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 5] against two baseline models: the original **U-Net** and a customized **wide U-Net** [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 5].

The reported liver segmentation results (measured in IoU: %) are [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 7]:

* **Baselines:**
  * **U-Net:** 76.62% (7.76M parameters)
  * **Wide U-Net:** 76.58% (9.13M parameters)
* **UNet++:**
  * **UNet++ without deep supervision (w/o DS):** 79.70% (9.04M parameters)
  * **UNet++ with deep supervision (w/ DS):** 82.90% (9.04M parameters)

**Retrieved from:**
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 7]
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 5]
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 1]
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 6]
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 2]
- [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 3]
- [ResUNet++: An Advanced Architecture for Medical Image Segmentation, page 1]
- [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]

## Q6. Which papers in this corpus report no liver segmentation result at all?

Based on the provided excerpts, there is no mention of which papers report no liver segmentation results at all. Therefore, the excerpts do not contain the answer to this question.

**Retrieved from:**
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 1]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 6]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 13]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 12]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 26]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 32]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 20]

## Q7. Compare CNN-based and transformer-based architectures on liver segmentation specifically.

Based on the provided excerpts, there is no information or comparison between CNN-based and transformer-based architectures on liver segmentation specifically.

**Retrieved from:**
- [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation, page 1]
- [Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation, page 9]
- [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation, page 2]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation, page 1]
- [UNETR: Transformers for 3D Medical Image Segmentation, page 1]
- [nnFormer: Interleaved Transformer for Volumetric Segmentation, page 1]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 15]

## Q8. How does H-DenseUNet relate to the Cascaded-FCN-liver paper?

Based on the provided excerpts, H-DenseUNet relates to the cascaded FCN approach by Christ et al. in the following ways:

* **Prior Work and 2D FCN Reference:** The H-DenseUNet paper cites Christ et al. as a deep learning-based method that proposed a cascaded FCN architecture and dense 3D conditional random fields (CRFs) to automatically segment the liver and liver lesions [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 3], noting it as an example of 2D FCN segmentation [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 2].
* **Cascaded Segmentation Strategy:** Both approaches utilize a cascaded strategy. In Christ et al., an initial FCN segments the liver to provide a region of interest (ROI) for a second FCN that segments lesions [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 1]. Similarly, H-DenseUNet employs a cascaded learning strategy where an initial ResNet is trained to obtain a quick, coarse liver segmentation ROI, within which H-DenseUNet performs accurate liver and lesion segmentation [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 3, 5].
* **Performance Comparison:** H-DenseUNet directly benchmarks its performance against Christ et al. on the 3DIRCADb dataset using cross-validation with matching training settings. H-DenseUNet outperformed Christ et al. on both lesion and liver segmentation accuracy, achieving a 9.0% and 0.4% improvement on DICE, respectively [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 8].

**Retrieved from:**
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 1]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 3]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 2]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 7]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 1]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 4]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 5]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 8]

## Q9. What does the Generalised Dice Loss paper contribute, and does it report a liver result?

Based on the provided excerpts, the contributions of the Generalised Dice Loss paper and the answer regarding liver results are as follows:

### Contributions of the Paper
* **Investigation of existing loss functions:** It investigates the training behavior of three previously published loss functions (such as weighted cross-entropy, sensitivity, and Dice loss) and assesses their robustness to learning rate tuning and sampling rates across 2D and 3D segmentation tasks under varying label imbalance [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 1].
* **Proposal of Generalized Dice Loss (GDL):** It proposes using the class re-balancing properties of the Generalized Dice overlap as a novel, robust, and accurate loss function for training deep convolutional neural networks on both balanced and unbalanced tasks [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 1, page 3].
* **Mathematical formulation and gradient derivation:** It defines the loss function formulation (including a weighting scheme, $\text{GDL}_v$, where weights are inversely proportional to volume squared to reduce the correlation between region size and Dice score) and provides its gradient for stochastic gradient descent [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 3].
* **Open-source release:** The studied loss functions were implemented and released as part of the open-source NiftyNet package [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 8].

### Liver Result
* The provided excerpts for this paper **do not** mention or report any liver results. The tasks and applications referenced in the text focus on brain tumors, white matter lesions, and future work on lacunes and perivascular spaces [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 1, page 8].

**Retrieved from:**
- [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 1]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 3]
- [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks, page 1]
- [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 8]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 3]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 18]
- [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 7]

## Q10. Across LiTS, the Decathlon, and KiTS19, how does organ segmentation difficulty compare to tumor segmentation difficulty?

Based on the provided excerpts, a comparison between organ segmentation difficulty and tumor segmentation difficulty is only provided for **LiTS** (which includes its participation in the **Medical Segmentation Decathlon** at MICCAI 2018); the excerpts do not contain comparative results for **KiTS19** or other Decathlon tasks.

For LiTS (and LiTS within the Decathlon):
* **Organ (liver) segmentation is substantially easier:** Most teams achieved high Dice scores above 0.930, with the best algorithm reaching 0.963 [The Liver Tumor Segmentation Benchmark (LiTS), page 3, 18]. State-of-the-art automated liver segmentation achieved performance similar to manual expert annotation, in part because the liver is a large organ [The Liver Tumor Segmentation Benchmark (LiTS), page 18].
* **Tumor segmentation is significantly more difficult:** The best tumor segmentation algorithms achieved much lower Dice scores of 0.674 (ISBI 2017), 0.702 (MICCAI 2017), and 0.739 (MICCAI 2018 / Decathlon) [The Liver Tumor Segmentation Benchmark (LiTS), page 3, 18]. Additionally, tumor detection recall was low (0.458 to 0.554), indicating an ongoing need for research [The Liver Tumor Segmentation Benchmark (LiTS), page 3].

For **KiTS19**, the excerpts mention that teams were ranked using the average Sørensen-Dice coefficient between kidneys and tumors, but do not provide comparative difficulty or performance data between the organ and the tumor [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge, page 3].

**Retrieved from:**
- [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge, page 3]
- [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge, page 1]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [A large annotated medical image dataset for the development and evaluation of segmentation algorithms, page 2]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 18]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 3]
- [A large annotated medical image dataset for the development and evaluation of segmentation algorithms, page 3]
- [The Medical Segmentation Decathlon, page 1]
