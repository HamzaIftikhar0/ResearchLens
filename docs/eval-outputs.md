# Eval run output (ungraded)

## Q1. What dataset did the U-Net paper evaluate on?

Based on the provided excerpts, the U-Net paper evaluated the network on the following tasks and datasets:

* **Segmentation of neuronal structures in electron microscopic recordings:** The data set is from the EM segmentation challenge started at ISBI 2012, consisting of 30 images (512x512 pixels) from serial section transmission electron microscopy of the Drosophila first instar larva ventral nerve cord (VNC) [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 6].
* **Cell segmentation in light microscopy images:** Part of the ISBI cell tracking challenge 2014 and 2015, which includes two data sets [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 7]:
  * The "PhC-U373" data set (Glioblastoma-astrocytoma U373 cells on a polyacrylimide substrate recorded by phase contrast microscopy), containing 35 partially annotated training images [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 7].
  * The "DIC-HeLa" data set (HeLa cells on a flat glass recorded by differential interference contrast microscopy), containing 20 partially annotated training images [U-Net: Convolutional Networks for Biomedical Image Segmentation, page 7].

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

Based on the provided excerpts, nnU-Net achieved a Liver Dice score of 0.93 during the development phase of the liver dataset in the Medical Segmentation Decathlon challenge [The Medical Segmentation Decathlon, page 33]. Additionally, in the Medical Segmentation Decathlon phase 1 tasks (run as five-fold cross-validation), the 3D U-Net (U-Net Cascade) achieved a Liver Dice score of 92.40 (or 92.64 when ensembled), the 3D U-Net achieved 92.45, the 2D U-Net achieved 77.42, and the test set achieved 68.16, as shown in Table 2 for the "Liver" task [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9].

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

Based on the provided excerpts, the comparison between U-Net and nnU-Net for liver segmentation is as follows:

* **Mean Dice Scores:** In phase 1 tasks (evaluated via five-fold cross-validation), the 2D U-Net achieved a Dice score of 77.42, the 3D U-Net achieved 79.07, and ensembles combining 2D U-Net with 3D U-Net (or U-Net Cascade) achieved 79.16 and 92.64 depending on the specific ensemble configuration [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, page 9]. 
* **Development Phase Performance (Liver Task):** In the Medical Segmentation Decathlon development phase liver dataset, the nnU-Net achieved a mean Dice similarity coefficient of 0.93 for the liver [The Medical Segmentation Decathlon, page 33].
* **General Framework and Adaptation:** nnU-Net is a self-adapting framework based on 2D and 3D vanilla U-Nets that automates pre-processing, training schemes, and inference with no manual interactions required between datasets [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation, pages 1, 9].

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

Based on the provided excerpts, the Attention U-Net adds novel attention gates (AGs) to the standard U-Net architecture [Attention U-Net: Learning Where to Look for the Pancreas, pages 1, 5]. These attention gates automatically learn to focus on target structures by highlighting salient features and suppressing irrelevant background regions, thereby eliminating the need for explicit external organ/tissue localisation modules [Attention U-Net: Learning Where to Look for the Pancreas, pages 1, 4]. 

Regarding the target organs, the Attention U-Net is evaluated on multi-class abdominal CT datasets for the segmentation of the **pancreas**, **spleen**, and **kidney** [Attention U-Net: Learning Where to Look for the Pancreas, pages 1, 6], with a primary focus and extensive evaluation on the challenging problem of **pancreas** segmentation (and boundary delineation) due to its low tissue contrast and large variability in shape and size [Attention U-Net: Learning Where to Look for the Pancreas, pages 2, 6].

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

Based on the provided excerpts, UNet++ reported the following liver results (measured by IoU: %) compared against U-Net and wide U-Net:

* **UNet++ w/o DS (without deep supervision):** 79.70% [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 7]
* **UNet++ w/ DS (with deep supervision):** 82.90% [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 7]
* **U-Net:** 76.62% [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 7]
* **Wide U-Net:** 76.58% [UNet++: A Nested U-Net Architecture for Medical Image Segmentation, page 7]

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

Based on the corpus summaries and excerpts, the following papers report **no liver segmentation result at all** (either because they focus entirely on other organs/modalities, or because they are dataset description/benchmark overview papers that do not evaluate a specific liver segmentation model):

1. **U-Net: Convolutional Networks for Biomedical Image Segmentation** – Evaluated exclusively on electron microscopy (EM) and cell tracking (PhC-U373, DIC-HeLa) datasets; states explicitly that the paper is not about liver segmentation [U-Net: Convolutional Networks for Biomedical Image Segmentation] (summary table).
2. **Attention U-Net: Learning Where to Look for the Pancreas** – Evaluated exclusively on pancreas CT datasets (CT-150 and TCIA Pancreas-CT); explicitly notes that no liver-specific segmentation performance is reported [Attention U-Net: Learning Where to Look for the Pancreas] (summary table).
3. **3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation** – Evaluated exclusively on Xenopus kidney embryo confocal microscopy volumes; states that it does not address liver segmentation [3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation] (summary table).
4. **V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation** – Evaluated exclusively on the PROMISE2012 prostate MRI challenge dataset [V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation] (summary table).
5. **TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation** – While it includes liver as one of 8 organs in the Synapse multi-organ CT dataset, the summary table and paper text indicate it is primarily a multi-organ/cardiac segmentation paper and does not report a standalone or dedicated liver segmentation result focus (though it reports a multi-organ liver DSC of 94.08%) [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation] (summary table). *Note: If counting purely "papers reporting no liver metric whatsoever," this paper does report a liver DSC, but several others completely omit the liver.* Let's check purely non-liver papers:
6. **ResUNet++: An Advanced Architecture for Medical Image Segmentation** – Evaluated exclusively on polyp/colonoscopy image datasets (Kvasir-SEG and CVC-ClinicDB); states it does not address liver segmentation [ResUNet++: An Advanced Architecture for Medical Image Segmentation] (summary table).
7. **DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation** – Evaluated on polyp detection, skin lesion (ISIC-2018), and cell nuclei datasets; not about liver segmentation [DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation] (summary table).
8. **3D MRI brain tumor segmentation using autoencoder regularization** – Evaluated exclusively on the BraTS 2018 brain MRI dataset; states it is about brain tumor segmentation, not liver segmentation [3D MRI brain tumor segmentation using autoencoder regularization] (summary table).
9. **Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations** – Evaluated on BRATS (brain tumor) and white matter hyperintensities datasets; not evaluated on liver segmentation [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations] (summary table).
10. **The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge** – Evaluated exclusively on kidney and kidney tumor CT scans (KiTS19 challenge) [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge] (summary table).
11. **A large annotated medical image dataset for the development and evaluation of segmentation algorithms** – This is purely a data descriptor paper releasing the Medical Segmentation Decathlon (MSD) repository and reports no model performance results at all [A large annotated medical image dataset for the development and evaluation of segmentation algorithms] (summary table).

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

Based on the corpus, CNN-based architectures (and hybrid CNN-Transformer models) have been extensively evaluated for liver segmentation specifically, while pure transformer-based architectures in this corpus (such as Swin-Unet and nnFormer) evaluate primarily on multi-organ or other abdominal CT datasets where liver segmentation is included as part of a larger multi-organ task (e.g., Synapse or BTCV datasets). 

Here is a comparison of their performance and characteristics regarding liver segmentation based on the provided sources:

### 1. CNN-Based Architectures
* **Performance:** Purely convolutional models and hybrid CNN architectures have established strong benchmarks for liver segmentation. 
  * **UNet++** with deep supervision achieved an IoU of **82.90%** on the MICCAI 2018 LiTS liver dataset, outperforming standard U-Net (76.62%) [UNet++: A Nested U-Net Architecture for Medical Image Segmentation].
  * **nnU-Net** achieved Dice scores of **90.37%** (class 1: liver) and **88.95%** (class 2: tumor) on the MSD Liver test set [nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation], and a mean DSC of **0.93** specifically for the liver across the MSD challenge [The Medical Segmentation Decathlon]. On the Synapse multi-organ dataset, the convolutional *nnUNet* achieved a liver DSC of **97.23%** (with a 1.62 mm HD95) [nnFormer: Interleaved Transformer for Volumetric Segmentation].
  * **H-DenseUNet** (combining 2D and 3D DenseUNet) achieved a liver Dice per case of **96.1%** (global Dice of **96.5%**) on the LiTS test dataset, and **98.2%** on the 3D-IRCADb dataset [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes].
  * **Cascaded Fully Convolutional Neural Networks (CFCN) + 3D CRF** achieved liver Dice scores of **94.3%** on 3DIRCADb, **91%** on a clinical CT dataset, and **87%** on clinical MR-DWI [Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks].
* **Characteristics & Limitations:** CNNs capture local spatial details effectively via hierarchical feature maps and skip connections. However, due to the intrinsic locality of convolution operations, they can struggle to capture explicit long-range contextual dependencies and are susceptible to over-segmentation when handling large anatomical variations [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation, page 1; Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation, page 9].

### 2. Transformer-Based Architectures (and Hybrids)
* **Performance:** Transformer-incorporated models have shown highly competitive or superior multi-organ segmentation results that include liver:
  * **TransUNet** (hybrid CNN-Transformer) achieved a liver-specific DSC of **94.08%** on the Synapse multi-organ CT dataset [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation].
  * **Swin-Unet** (pure Transformer U-Net) achieved a liver-specific DSC of **94.29%** on the Synapse dataset [Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation].
  * **nnFormer** (interleaved 3D transformer and convolution) achieved a liver segmentation DSC of **96.84%** (with an HD95 of 2.00 mm) on the Synapse dataset [nnFormer: Interleaved Transformer for Volumetric Segmentation].
  * **UNETR** (transformer encoder with CNN decoder) achieved a liver-specific Dice score of **0.971** on the BTCV standard competition [UNETR: Transformers for 3D Medical Image Segmentation].
* **Characteristics & Limitations:** Transformers excel at modeling global contexts and long-range dependencies through self-attention mechanisms [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation, page 2]. However, pure transformer models (like Swin-Unet) or heavy transformer components are limited by high GPU memory consumption [UNETR: Transformers for 3D Medical Image Segmentation] and can underperform compared to heavily optimized CNN baselines (such as nnUNet) on certain organ structures like the liver unless carefully structured or ensembled [nnFormer: Interleaved Transformer for Volumetric Segmentation].

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

Based on the provided excerpts, the "Cascaded-FCN-liver" paper (titled *Automatic Liver and Tumor Segmentation of CT and MRI Volumes Using Cascaded Fully Convolutional Neural Networks* by Patrick Ferdinand Christ et al.) relates to H-DenseUNet in the following ways:

* **Comparison of Dataset Results:** H-DenseUNet's performance on the 3DIRCADb dataset was directly compared against the state-of-the-art method from Christ et al. ([H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 8]). Through cross-validation experiments, H-DenseUNet achieved better performance than the method by Christ et al. on both lesion and liver segmentation accuracy, showing improvements of 9.0% and 0.4% on DICE, respectively [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 8]. 
* **Prior Literature on Cascaded FCNs:** The paper by Christ et al. is cited as an example of deep learning-based methods where a cascaded FCN architecture and dense 3D conditional random fields (CRFs) are used to automatically segment the liver and its lesions [H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes, page 3].

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

Based on the provided excerpts, the Generalized Dice Loss paper proposes using the class re-balancing properties of the Generalized Dice overlap as a novel deep-learning loss function for both balanced and unbalanced data, and investigates the training behavior of loss functions in different multi-class segmentation problems [Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, page 1]. 

The provided excerpts do not contain the answer regarding whether the paper reports a liver result.

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

Based on the provided corpus (including summaries and excerpts for LiTS, the Medical Segmentation Decathlon, and KiTS19), organ segmentation is consistently and substantially easier than tumor segmentation across all three benchmarks. 

### 1. The Liver Tumor Segmentation Benchmark (LiTS)
* **Liver (Organ) Segmentation:** The best-performing algorithms achieve exceptional accuracy, with the top liver segmentation algorithm reaching a Dice score of **0.963** [The Liver Tumor Segmentation Benchmark, page 3]. Most participating teams scored above 0.930 [The Liver Tumor Segmentation Benchmark, page 18].
* **Tumor Segmentation:** In contrast, tumor segmentation proves significantly more difficult. The best algorithms achieved much lower Dice scores across the three events: **0.674** (ISBI 2017), **0.702** (MICCAI 2017), and **0.739** (MICCAI 2018) [The Liver Tumor Segmentation Benchmark, page 3]. Furthermore, methods struggled immensely with tumor detection, with the best methods only achieving a lesion-wise recall between 0.458 and 0.554 [The Liver Tumor Segmentation Benchmark, page 3], largely because algorithms struggle with small tumors under 10 mm and low-contrast regions [The Liver Tumor Segmentation Benchmark].

### 2. The Medical Segmentation Decathlon (MSD)
* **Liver (Organ) Segmentation:** When evaluated on liver segmentation specifically (Task03_Liver), top-performing frameworks like nnU-Net achieved a high mean Dice Similarity Coefficient (DSC) of **0.93** [The Medical Segmentation Decathlon]. Other models like H-DenseUNet and UNet++ achieved liver Dice scores/IoUs of 96.1% and 82.90% respectively [H-DenseUNet, UNet++].
* **Tumor Segmentation:** Tumor segmentation on the same dataset is considerably harder, with the leading methods only achieving a mean DSC of **0.74** for liver tumors [The Medical Segmentation Decathlon].

### 3. The KiTS19 Challenge (Kidney and Kidney Tumor Segmentation)
* **Kidney (Organ) Segmentation:** Similar to the liver, the winning teams on the KiTS19 challenge achieved near-perfect segmentation for the host organ, obtaining a Dice score of **0.974** for the kidney [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge].
* **Tumor Segmentation:** Tumor segmentation scores lagged significantly behind, with the winning team achieving a Dice score of **0.851** for the kidney tumor [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge]. 

**Summary:** Across all three challenges (LiTS, Decathlon, and KiTS19), host organs (liver and kidneys) are large and structurally consistent enough that top deep-learning models easily achieve Dice scores upwards of 0.93 to 0.97. Tumors, however, suffer from high variability in size, shape, multi-focal appearance, and low contrast (such as small lesions under 10 mm), resulting in dramatically lower Dice scores (typically 0.67 to 0.85) and proving to be a much more difficult segmentation task [The Liver Tumor Segmentation Benchmark, The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge].

**Retrieved from:**
- [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge, page 3]
- [The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge, page 1]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 5]
- [A large annotated medical image dataset for the development and evaluation of segmentation algorithms, page 2]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 18]
- [The Liver Tumor Segmentation Benchmark (LiTS), page 3]
- [A large annotated medical image dataset for the development and evaluation of segmentation algorithms, page 3]
- [The Medical Segmentation Decathlon, page 1]
