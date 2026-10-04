"""Extract corpus/*.pdf page by page, embed each page, save the Phase 0 index.

One embed_content call per page (a list of texts in one call returns a
single combined embedding, not one per page - confirmed by testing). Saves
after every page and skips pages already in the index, so a 429 mid-run
costs a retry, not the whole corpus.

Run: python -m app.ingest.build_index
"""

from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from google import genai

from app.ingest.embeddings import embed_text
from app.ingest.index_store import load_index, save_index

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parents[2]
CORPUS_DIR = BACKEND_DIR.parent / "corpus"

CORPUS = {
    "unet": {
        "filename": "unet-1505.04597.pdf",
        "title": "U-Net: Convolutional Networks for Biomedical Image Segmentation",
    },
    "attention-unet": {
        "filename": "attention-unet-1804.03999.pdf",
        "title": "Attention U-Net: Learning Where to Look for the Pancreas",
    },
    "unetpp": {
        "filename": "unetpp-1807.10165.pdf",
        "title": "UNet++: A Nested U-Net Architecture for Medical Image Segmentation",
    },
    "nnunet": {
        "filename": "nnunet-1809.10486.pdf",
        "title": "nnU-Net: Self-adapting Framework for U-Net-Based Medical Image Segmentation",
    },
    "lits": {
        "filename": "lits-1901.04056.pdf",
        "title": "The Liver Tumor Segmentation Benchmark (LiTS)",
    },
    "3dunet": {
        "filename": "3dunet-1606.06650.pdf",
        "title": "3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation",
    },
    "vnet": {
        "filename": "vnet-1606.04797.pdf",
        "title": "V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation",
    },
    "hdenseunet": {
        "filename": "hdenseunet-1709.07330.pdf",
        "title": "H-DenseUNet: Hybrid Densely Connected UNet for Liver and Tumor Segmentation from CT Volumes",
    },
    "cascadedfcn-liver": {
        "filename": "cascadedfcn-liver-1702.05970.pdf",
        "title": "Automatic Liver and Tumor Segmentation of CT and MRI Volumes using Cascaded Fully Convolutional Neural Networks",
    },
    "msd": {
        "filename": "msd-2106.05735.pdf",
        "title": "The Medical Segmentation Decathlon",
    },
    "msd-dataset": {
        "filename": "msd-dataset-1902.09063.pdf",
        "title": "A large annotated medical image dataset for the development and evaluation of segmentation algorithms",
    },
    "transunet": {
        "filename": "transunet-2102.04306.pdf",
        "title": "TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation",
    },
    "swinunet": {
        "filename": "swinunet-2105.05537.pdf",
        "title": "Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation",
    },
    "nnformer": {
        "filename": "nnformer-2109.03201.pdf",
        "title": "nnFormer: Interleaved Transformer for Volumetric Segmentation",
    },
    "unetr": {
        "filename": "unetr-2103.10504.pdf",
        "title": "UNETR: Transformers for 3D Medical Image Segmentation",
    },
    "resunetpp": {
        "filename": "resunetpp-1911.07067.pdf",
        "title": "ResUNet++: An Advanced Architecture for Medical Image Segmentation",
    },
    "doubleunet": {
        "filename": "doubleunet-2006.04868.pdf",
        "title": "DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation",
    },
    "segresnet": {
        "filename": "segresnet-1810.11654.pdf",
        "title": "3D MRI brain tumor segmentation using autoencoder regularization",
    },
    "gdl": {
        "filename": "gdl-1707.03237.pdf",
        "title": "Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations",
    },
    "kits19": {
        "filename": "kits19-1912.01054.pdf",
        "title": "The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge",
    },
    # --- Phase 1B: 20 -> ~100 papers (52 new, below) ---
    "liver-curriculum": {
        "filename": "liver-curriculum-1910.07895.pdf",
        "title": "A New Three-stage Curriculum Learning Approach to Deep Network Based Liver Tumor Segmentation",
    },
    "liver-joint-dl": {
        "filename": "liver-joint-dl-1902.07971.pdf",
        "title": "A Joint Deep Learning Approach for Automated Liver and Tumor Segmentation",
    },
    "liver-nn-rf-filter": {
        "filename": "liver-nn-rf-filter-1706.00842.pdf",
        "title": "Neural Network-Based Automatic Liver Tumor Segmentation With Random Forest-Based Candidate Filtering",
    },
    "liver-hierarchical-convdeconv": {
        "filename": "liver-hierarchical-convdeconv-1710.04540.pdf",
        "title": "Hierarchical Convolutional-Deconvolutional Neural Networks for Automatic Liver and Tumor Segmentation",
    },
    "liver-lesion-joint": {
        "filename": "liver-lesion-joint-1707.07734.pdf",
        "title": "Liver lesion segmentation informed by joint liver segmentation",
    },
    "kidney-liver-tumor-seg": {
        "filename": "kidney-liver-tumor-seg-1908.01279.pdf",
        "title": "Automatic segmentation of kidney and liver tumors in CT images",
    },
    "liver-efficient-3dcnn": {
        "filename": "liver-efficient-3dcnn-2208.13271.pdf",
        "title": "Efficient liver segmentation with 3D CNN using computed tomography scans",
    },
    "liver-2d-denseunet": {
        "filename": "liver-2d-denseunet-1802.02182.pdf",
        "title": "2D-Densely Connected Convolution Neural Networks for automatic Liver and Tumor Segmentation",
    },
    "liver-fibrosis-radiomics": {
        "filename": "liver-fibrosis-radiomics-2211.14396.pdf",
        "title": "Non-invasive Liver Fibrosis Screening on CT Images using Radiomics",
    },
    "liver-cirrhosis-mri": {
        "filename": "liver-cirrhosis-mri-2502.18225.pdf",
        "title": "Liver Cirrhosis Stage Estimation from MRI with Deep Learning",
    },
    "medical-transformer-axial": {
        "filename": "medical-transformer-axial-2102.10662.pdf",
        "title": "Medical Transformer: Gated Axial-Attention for Medical Image Segmentation",
    },
    "convolution-free-medseg": {
        "filename": "convolution-free-medseg-2102.13645.pdf",
        "title": "Convolution-Free Medical Image Segmentation using Transformers",
    },
    "medsam": {
        "filename": "medsam-2304.12306.pdf",
        "title": "Segment Anything in Medical Images",
    },
    "selfsup-pretrain-2d-medseg": {
        "filename": "selfsup-pretrain-2d-medseg-2209.00314.pdf",
        "title": "Self-Supervised Pretraining for 2D Medical Image Segmentation",
    },
    "selfsup-rcnn-medseg": {
        "filename": "selfsup-rcnn-medseg-2207.11191.pdf",
        "title": "Self-Supervised-RCNN for Medical Image Segmentation with Limited Data Annotation",
    },
    "mis-fm": {
        "filename": "mis-fm-2306.16925.pdf",
        "title": "MIS-FM: 3D Medical Image Segmentation using Foundation Models Pretrained on a Large-Scale Unannotated Dataset",
    },
    "nnunet-revisited": {
        "filename": "nnunet-revisited-2404.09556.pdf",
        "title": "nnU-Net Revisited: A Call for Rigorous Validation in 3D Medical Image Segmentation",
    },
    "boundary-loss": {
        "filename": "boundary-loss-1812.07032.pdf",
        "title": "Boundary loss for highly unbalanced segmentation",
    },
    "contrastive-domain-disentangle": {
        "filename": "contrastive-domain-disentangle-2205.06551.pdf",
        "title": "Contrastive Domain Disentanglement for Generalizable Medical Image Segmentation",
    },
    "cddsa": {
        "filename": "cddsa-2211.12081.pdf",
        "title": "CDDSA: Contrastive Domain Disentanglement and Style Augmentation for Generalizable Medical Image Segmentation",
    },
    "deepedit": {
        "filename": "deepedit-2305.10655.pdf",
        "title": "DeepEdit: Deep Editable Learning for Interactive Segmentation of 3D Medical Images",
    },
    "bayesian-uncertainty-nnunet": {
        "filename": "bayesian-uncertainty-nnunet-2212.06278.pdf",
        "title": "Efficient Bayesian Uncertainty Estimation for nnU-Net",
    },
    "every-annotation-counts": {
        "filename": "every-annotation-counts-2104.13243.pdf",
        "title": "Every Annotation Counts: Multi-label Deep Supervision for Medical Image Segmentation",
    },
    "resnet": {
        "filename": "resnet-1512.03385.pdf",
        "title": "Deep Residual Learning for Image Recognition",
    },
    "densenet": {
        "filename": "densenet-1608.06993.pdf",
        "title": "Densely Connected Convolutional Networks",
    },
    "batchnorm": {
        "filename": "batchnorm-1502.03167.pdf",
        "title": "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
    },
    "vit": {
        "filename": "vit-2010.11929.pdf",
        "title": "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
    },
    "swin-transformer": {
        "filename": "swin-transformer-2103.14030.pdf",
        "title": "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows",
    },
    "focal-loss": {
        "filename": "focal-loss-1708.02002.pdf",
        "title": "Focal Loss for Dense Object Detection",
    },
    "attention-is-all-you-need": {
        "filename": "attention-is-all-you-need-1706.03762.pdf",
        "title": "Attention Is All You Need",
    },
    "cardiac-seg-review": {
        "filename": "cardiac-seg-review-1911.03723.pdf",
        "title": "Deep learning for cardiac image segmentation: A review",
    },
    "cardiac-2d3d-exploration": {
        "filename": "cardiac-2d3d-exploration-1709.04496.pdf",
        "title": "An Exploration of 2D and 3D Deep Learning Techniques for Cardiac MR Image Segmentation",
    },
    "isles2022-stroke-dataset": {
        "filename": "isles2022-stroke-dataset-2206.06694.pdf",
        "title": "ISLES 2022: A multi-center magnetic resonance imaging stroke lesion segmentation dataset",
    },
    "embracing-imperfect-datasets": {
        "filename": "embracing-imperfect-datasets-1908.10454.pdf",
        "title": "Embracing Imperfect Datasets: A Review of Deep Learning Solutions for Medical Image Segmentation",
    },
    "multitask-medseg": {
        "filename": "multitask-medseg-1704.03379.pdf",
        "title": "Deep Learning for Multi-Task Medical Image Segmentation in Multiple Modalities",
    },
    "pvtformer-liver": {
        "filename": "pvtformer-liver-2401.09630.pdf",
        "title": "CT Liver Segmentation via PVT-based Encoding and Refined Decoding",
    },
    "gan-medical-imaging-review": {
        "filename": "gan-medical-imaging-review-1809.07294.pdf",
        "title": "Generative Adversarial Network in Medical Imaging: A Review",
    },
    "vgg": {
        "filename": "vgg-1409.1556.pdf",
        "title": "Very Deep Convolutional Networks for Large-Scale Image Recognition",
    },
    "adam-optimizer": {
        "filename": "adam-optimizer-1412.6980.pdf",
        "title": "Adam: A Method for Stochastic Optimization",
    },
    "squeeze-excitation": {
        "filename": "squeeze-excitation-1709.01507.pdf",
        "title": "Squeeze-and-Excitation Networks",
    },
    "fcn-semantic-seg": {
        "filename": "fcn-semantic-seg-1605.06211.pdf",
        "title": "Fully Convolutional Networks for Semantic Segmentation",
    },
    "deeplab": {
        "filename": "deeplab-1606.00915.pdf",
        "title": "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs",
    },
    "unet-knowledge-distillation": {
        "filename": "unet-knowledge-distillation-1812.00249.pdf",
        "title": "On Compressing U-net Using Knowledge Distillation",
    },
    "3d-ux-net": {
        "filename": "3d-ux-net-2209.15076.pdf",
        "title": "3D UX-Net: A Large Kernel Volumetric ConvNet Modernizing Hierarchical Transformer for Medical Image Segmentation",
    },
    "sparse-annotation-active-learning": {
        "filename": "sparse-annotation-active-learning-1906.07367.pdf",
        "title": "A sparse annotation strategy based on attention-guided active learning for 3D medical image segmentation",
    },
    "interpretability-review": {
        "filename": "interpretability-review-2111.02398.pdf",
        "title": "Transparency of Deep Neural Networks for Medical Image Analysis: A Review of Interpretability Methods",
    },
    "covid-comparative-study": {
        "filename": "covid-comparative-study-2007.15546.pdf",
        "title": "Comparative study of deep learning methods for the automatic segmentation of lung, lesion and lesion type in CT scans of COVID-19 patients",
    },
    "covid-lung-lesion-maskrcnn": {
        "filename": "covid-lung-lesion-maskrcnn-2105.08147.pdf",
        "title": "COVID-19 Lung Lesion Segmentation Using a Sparsely Supervised Mask R-CNN on Chest X-rays Automatically Computed from Volumetric CTs",
    },
    "prostate-zonal-seg": {
        "filename": "prostate-zonal-seg-1911.00127.pdf",
        "title": "Automatic Prostate Zonal Segmentation Using Fully Convolutional Network with Feature Pyramid Attention",
    },
    "amos-multiorgan-benchmark": {
        "filename": "amos-multiorgan-benchmark-2206.08023.pdf",
        "title": "AMOS: A Large-Scale Abdominal Multi-Organ Benchmark for Versatile Medical Image Segmentation",
    },
    "abdomenct1k": {
        "filename": "abdomenct1k-2010.14808.pdf",
        "title": "AbdomenCT-1K: Is Abdominal Organ Segmentation A Solved Problem?",
    },
    "deeplabv3": {
        "filename": "deeplabv3-1706.05587.pdf",
        "title": "Rethinking Atrous Convolution for Semantic Image Segmentation",
    },
}


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    doc = pymupdf.open(pdf_path)
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append((i, text))
    return pages


def main() -> None:
    client = genai.Client()

    try:
        chunks = load_index()
    except FileNotFoundError:
        chunks = []
    done = {(c["paper"], c["page"]) for c in chunks}

    for key, meta in CORPUS.items():
        pages = extract_pages(CORPUS_DIR / meta["filename"])
        new_pages = [p for p in pages if (key, p[0]) not in done]
        if not new_pages:
            print(f"{key}: already indexed ({len(pages)} pages)")
            continue

        for page_num, text in new_pages:
            vector = embed_text(client, text, task_type="RETRIEVAL_DOCUMENT")
            chunks.append({
                "paper": key,
                "title": meta["title"],
                "page": page_num,
                "text": text,
                "vector": vector,
            })
            save_index(chunks)
            print(f"{key}: page {page_num}/{pages[-1][0]} indexed")

    print(f"\n{len(chunks)} chunks in the index")


if __name__ == "__main__":
    main()
