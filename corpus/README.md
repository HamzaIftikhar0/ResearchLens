# Test corpus

Five open-access papers from arXiv, used as the liver-segmentation test
library described in [PLAN.md](../PLAN.md) section 3. Committed to the repo
on purpose — they're open-access preprints, so there's no copyright blocker
to a public demo (see PLAN.md section 11, Risks).

| File | arXiv ID | Title |
|---|---|---|
| `unet-1505.04597.pdf` | [1505.04597](https://arxiv.org/abs/1505.04597) | U-Net: Convolutional Networks for Biomedical Image Segmentation |
| `attention-unet-1804.03999.pdf` | [1804.03999](https://arxiv.org/abs/1804.03999) | Attention U-Net: Learning Where to Look for the Pancreas |
| `unetpp-1807.10165.pdf` | [1807.10165](https://arxiv.org/abs/1807.10165) | UNet++: A Nested U-Net Architecture for Medical Image Segmentation |
| `nnunet-1809.10486.pdf` | [1809.10486](https://arxiv.org/abs/1809.10486) | nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation |
| `lits-1901.04056.pdf` | [1901.04056](https://arxiv.org/abs/1901.04056) | The Liver Tumor Segmentation Benchmark (LiTS) |

More open-access papers can be added the same way (verify the arXiv ID
resolves to the expected title before adding). The 100-paper target in
PLAN.md section 2 doesn't need to be hit before Phase 0 — 5 is enough to
prove the pipeline.
