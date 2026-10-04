# Test corpus

Seventy-two open-access papers from arXiv: the original 20-paper Phase 1A
set below, plus 52 more added for Phase 1B (section further down). Used as
the liver-segmentation test library described in [PLAN.md](../PLAN.md)
section 3. Committed to the repo on purpose — they're open-access
preprints, so there's no copyright blocker to a public demo (see PLAN.md
section 10, Risks).

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

## Phase 1B additions (52 papers)

Found via web search rather than recalled from memory — at this volume,
memory alone would have been unreliable — and every arXiv ID was still
verified against its actual abstract-page title before downloading, same
discipline as the original 20. Grouped by theme rather than one 72-row
table.

**Liver-specific (10):** curriculum learning ([1910.07895](https://arxiv.org/abs/1910.07895)), joint liver+tumor FCNs ([1902.07971](https://arxiv.org/abs/1902.07971)), NN + random-forest candidate filtering ([1706.00842](https://arxiv.org/abs/1706.00842)), hierarchical conv-deconv ([1710.04540](https://arxiv.org/abs/1710.04540)), lesion segmentation informed by liver segmentation ([1707.07734](https://arxiv.org/abs/1707.07734)), joint kidney+liver tumor segmentation ([1908.01279](https://arxiv.org/abs/1908.01279)), efficient 3D CNN liver segmentation ([2208.13271](https://arxiv.org/abs/2208.13271)), 2D dense-connected liver+tumor ([1802.02182](https://arxiv.org/abs/1802.02182)), liver fibrosis radiomics screening ([2211.14396](https://arxiv.org/abs/2211.14396)), liver cirrhosis staging from MRI ([2502.18225](https://arxiv.org/abs/2502.18225)), and a 2024 PVT-based transformer liver segmenter ([2401.09630](https://arxiv.org/abs/2401.09630)).

**Foundation models / self-supervised (5):** MedSAM ([2304.12306](https://arxiv.org/abs/2304.12306)), MIS-FM foundation-model pretraining ([2306.16925](https://arxiv.org/abs/2306.16925)), self-supervised 2D pretraining ([2209.00314](https://arxiv.org/abs/2209.00314)), self-supervised-RCNN for limited annotation ([2207.11191](https://arxiv.org/abs/2207.11191)), knowledge distillation for U-Net compression ([1812.00249](https://arxiv.org/abs/1812.00249)).

**Architectures beyond the Phase 1A set (5):** Medical Transformer / gated axial attention ([2102.10662](https://arxiv.org/abs/2102.10662)), convolution-free segmentation ([2102.13645](https://arxiv.org/abs/2102.13645)), 3D UX-Net ([2209.15076](https://arxiv.org/abs/2209.15076)), nnU-Net Revisited ([2404.09556](https://arxiv.org/abs/2404.09556)), DeepEdit interactive segmentation ([2305.10655](https://arxiv.org/abs/2305.10655)).

**Training techniques / robustness (6):** Boundary loss ([1812.07032](https://arxiv.org/abs/1812.07032)), contrastive domain disentanglement ([2205.06551](https://arxiv.org/abs/2205.06551)), CDDSA domain generalization ([2211.12081](https://arxiv.org/abs/2211.12081)), Bayesian uncertainty for nnU-Net ([2212.06278](https://arxiv.org/abs/2212.06278)), multi-label deep supervision ([2104.13243](https://arxiv.org/abs/2104.13243)), sparse-annotation active learning ([1906.07367](https://arxiv.org/abs/1906.07367)).

**Benchmarks, datasets, and application domains beyond liver (10):** cardiac segmentation review ([1911.03723](https://arxiv.org/abs/1911.03723)) and 2D/3D exploration ([1709.04496](https://arxiv.org/abs/1709.04496)), ISLES 2022 stroke dataset ([2206.06694](https://arxiv.org/abs/2206.06694)), multi-task multi-modality segmentation ([1704.03379](https://arxiv.org/abs/1704.03379)), 2 COVID-19 CT segmentation studies ([2007.15546](https://arxiv.org/abs/2007.15546), [2105.08147](https://arxiv.org/abs/2105.08147)), prostate zonal segmentation ([1911.00127](https://arxiv.org/abs/1911.00127)), AMOS multi-organ benchmark — liver is 1 of 15 organs ([2206.08023](https://arxiv.org/abs/2206.08023)), AbdomenCT-1K ([2010.14808](https://arxiv.org/abs/2010.14808)), GAN-in-medical-imaging review ([1809.07294](https://arxiv.org/abs/1809.07294)).

**Surveys (1):** "Embracing Imperfect Datasets" ([1908.10454](https://arxiv.org/abs/1908.10454)), "Transparency of DNNs for Medical Image Analysis" ([2111.02398](https://arxiv.org/abs/2111.02398)).

**Foundational background papers (15):** things the Phase 1A corpus already builds on without being in it — ResNet ([1512.03385](https://arxiv.org/abs/1512.03385)), DenseNet ([1608.06993](https://arxiv.org/abs/1608.06993)), Batch Normalization ([1502.03167](https://arxiv.org/abs/1502.03167)), VGG ([1409.1556](https://arxiv.org/abs/1409.1556)), ViT ([2010.11929](https://arxiv.org/abs/2010.11929)), Swin Transformer ([2103.14030](https://arxiv.org/abs/2103.14030)), Attention Is All You Need ([1706.03762](https://arxiv.org/abs/1706.03762)), Focal Loss ([1708.02002](https://arxiv.org/abs/1708.02002)), Adam ([1412.6980](https://arxiv.org/abs/1412.6980)), Squeeze-and-Excitation ([1709.01507](https://arxiv.org/abs/1709.01507)), FCN for semantic segmentation ([1605.06211](https://arxiv.org/abs/1605.06211)), DeepLab ([1606.00915](https://arxiv.org/abs/1606.00915)) and DeepLabv3/ASPP ([1706.05587](https://arxiv.org/abs/1706.05587)).

Exact filenames and the manifest (key, filename, title) used for indexing
live in `backend/app/ingest/build_index.py`'s `CORPUS` dict — that file is
the source of truth, this README is the human-readable summary.

Stopped deliberately at 72, not forced to exactly 100 — PLAN.md's own
caution against "collect as many papers as possible": the goal was a
materially larger corpus (3.6x) to stress-test retrieval at scale, not a
round number. More can be added the same way (web search or memory, always
verified against the actual abstract-page title before downloading) if a
future phase wants to push further.
