# Test corpus

Twenty open-access papers from arXiv, used as the liver-segmentation test
library described in [PLAN.md](../PLAN.md) section 3. Committed to the repo
on purpose — they're open-access preprints, so there's no copyright blocker
to a public demo (see PLAN.md section 10, Risks).

Not every paper is about liver segmentation specifically — several are
foundational architectures, benchmark/dataset papers, or method papers (loss
functions) that get applied to liver segmentation in practice without being
liver papers themselves. That's deliberate: `docs/answer-key.md` uses the
gap to test whether the pipeline invents results instead of reporting what's
actually in a paper.

| File | arXiv ID | Title | Liver-specific? |
|---|---|---|---|
| `unet-1505.04597.pdf` | [1505.04597](https://arxiv.org/abs/1505.04597) | U-Net: Convolutional Networks for Biomedical Image Segmentation | No — EM/cell-tracking only |
| `attention-unet-1804.03999.pdf` | [1804.03999](https://arxiv.org/abs/1804.03999) | Attention U-Net: Learning Where to Look for the Pancreas | No — pancreas is the headline organ |
| `unetpp-1807.10165.pdf` | [1807.10165](https://arxiv.org/abs/1807.10165) | UNet++: A Nested U-Net Architecture for Medical Image Segmentation | Yes — one of 4 datasets (LiTS) |
| `nnunet-1809.10486.pdf` | [1809.10486](https://arxiv.org/abs/1809.10486) | nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation | Yes — one of 7 Decathlon tasks |
| `lits-1901.04056.pdf` | [1901.04056](https://arxiv.org/abs/1901.04056) | The Liver Tumor Segmentation Benchmark (LiTS) | Yes — the benchmark itself |
| `3dunet-1606.06650.pdf` | [1606.06650](https://arxiv.org/abs/1606.06650) | 3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation | No — Xenopus kidney microscopy |
| `vnet-1606.04797.pdf` | [1606.04797](https://arxiv.org/abs/1606.04797) | V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation | No — prostate MRI only |
| `hdenseunet-1709.07330.pdf` | [1709.07330](https://arxiv.org/abs/1709.07330) | H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes | Yes — LiTS + 3DIRCADb |
| `cascadedfcn-liver-1702.05970.pdf` | [1702.05970](https://arxiv.org/abs/1702.05970) | Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks | Yes |
| `msd-2106.05735.pdf` | [2106.05735](https://arxiv.org/abs/2106.05735) | The Medical Segmentation Decathlon | Yes — Liver is one of 10 tasks |
| `msd-dataset-1902.09063.pdf` | [1902.09063](https://arxiv.org/abs/1902.09063) | A large annotated medical image dataset for the development and evaluation of segmentation algorithms | Yes — dataset description, no results |
| `transunet-2102.04306.pdf` | [2102.04306](https://arxiv.org/abs/2102.04306) | TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation | Yes — one of 8 Synapse organs |
| `swinunet-2105.05537.pdf` | [2105.05537](https://arxiv.org/abs/2105.05537) | Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation | Yes — one of 8 Synapse organs |
| `nnformer-2109.03201.pdf` | [2109.03201](https://arxiv.org/abs/2109.03201) | nnFormer: Interleaved Transformer for Volumetric Segmentation | Yes — one of 8 Synapse organs |
| `unetr-2103.10504.pdf` | [2103.10504](https://arxiv.org/abs/2103.10504) | UNETR: Transformers for 3D Medical Image Segmentation | Yes — one of 13 BTCV organs |
| `resunetpp-1911.07067.pdf` | [1911.07067](https://arxiv.org/abs/1911.07067) | ResUNet++: An Advanced Architecture for Medical Image Segmentation | No — colonoscopy polyps only |
| `doubleunet-2006.04868.pdf` | [2006.04868](https://arxiv.org/abs/2006.04868) | DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation | No — polyps/skin lesions/nuclei only |
| `segresnet-1810.11654.pdf` | [1810.11654](https://arxiv.org/abs/1810.11654) | 3D MRI brain tumor segmentation using autoencoder regularization | No — brain tumor (BraTS) only |
| `gdl-1707.03237.pdf` | [1707.03237](https://arxiv.org/abs/1707.03237) | Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations | No — a loss-function study (brain tumor, white-matter lesions), not an architecture or application paper |
| `kits19-1912.01054.pdf` | [1912.01054](https://arxiv.org/abs/1912.01054) | The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge | No — kidney, not liver (same organ-vs-tumor difficulty gap as LiTS, different organ) |

More open-access papers can be added the same way (verify the arXiv ID
resolves to the expected title before adding). The ~100-paper target in
PLAN.md section 2 is the Phase 1B target; this 20-paper set is Phase 1A —
see PLAN.md section 7.
