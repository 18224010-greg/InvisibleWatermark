import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

OUT = Path("hasil_watermarking")
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

def load_rgb(path):
    return np.array(Image.open(path).convert("RGB"))

def load_gray(path):
    return np.array(Image.open(path).convert("L"))

def save_fig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()

original = load_rgb(OUT / "01_foto_asli.png")
watermark = load_gray(OUT / "02_watermark_asli.png")
watermarked = load_rgb(OUT / "03_foto_berwatermark_lossless.png")
qf100 = load_rgb(OUT / "foto_berwatermark_QF_100.jpg")
extract_lossless = load_gray(OUT / "04_watermark_ekstrak_lossless.png")
extract_qf100 = load_gray(OUT / "watermark_ekstrak_QF_100.png")
extract_qf30 = load_gray(OUT / "watermark_ekstrak_QF_30.png")
extract_qf5 = load_gray(OUT / "watermark_ekstrak_QF_5.png")

gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(original)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(gray, cmap="gray")
plt.title("Luminance / Grayscale")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(gray, cmap="gray")
for i in range(0, gray.shape[0], 8):
    plt.axhline(i, color="red", linewidth=0.25, alpha=0.5)
    plt.axvline(i, color="red", linewidth=0.25, alpha=0.5)
plt.title("8×8 Block Grid")
plt.axis("off")
save_fig(DOCS / "step1_preprocessing.png")

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(watermark, cmap="gray")
plt.title("Binary Watermark 32×32")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(watermark, cmap="gray", interpolation="nearest")
for i in range(0, watermark.shape[0] + 1):
    plt.axhline(i - 0.5, color="gray", linewidth=0.3)
    plt.axvline(i - 0.5, color="gray", linewidth=0.3)
plt.title("Watermark Bit Pattern")
plt.axis("off")
save_fig(DOCS / "step2_watermark.png")

block = gray[120:128, 120:128].astype(np.float32) - 128
dct_block = cv2.dct(block)
dct_log = np.log(np.abs(dct_block) + 1)

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(block + 128, cmap="gray")
plt.title("Sample 8×8 Block")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(dct_log, cmap="inferno")
plt.title("DCT Coefficients")
plt.colorbar(fraction=0.046, pad=0.04)
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(dct_log, cmap="inferno")
plt.scatter([1, 2], [4, 3], s=180, facecolors="none", edgecolors="cyan", linewidths=2)
plt.title("Embedding Coefficients")
plt.axis("off")
save_fig(DOCS / "step3_dct_embedding.png")

diff_watermark = np.abs(original.astype(np.int16) - watermarked.astype(np.int16)).mean(axis=2)
diff_qf100 = np.abs(original.astype(np.int16) - qf100.astype(np.int16)).mean(axis=2)

plt.figure(figsize=(14, 4))
plt.subplot(1, 4, 1)
plt.imshow(original)
plt.title("Before Watermarking")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(watermarked)
plt.title("After Watermarking")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.imshow(qf100)
plt.title("After Watermarking + JPEG QF 100")
plt.axis("off")

plt.subplot(1, 4, 4)
plt.imshow(diff_qf100, cmap="hot")
plt.title("Difference Map")
plt.colorbar(fraction=0.046, pad=0.04)
plt.axis("off")
save_fig(DOCS / "step4_before_after_qf100.png")

plt.figure(figsize=(12, 4))
plt.subplot(1, 4, 1)
plt.imshow(watermark, cmap="gray")
plt.title("Original WM")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(extract_qf100, cmap="gray")
plt.title("Extracted QF 100")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.imshow(extract_qf30, cmap="gray")
plt.title("Extracted QF 30")
plt.axis("off")

plt.subplot(1, 4, 4)
plt.imshow(extract_qf5, cmap="gray")
plt.title("Extracted QF 5")
plt.axis("off")
save_fig(DOCS / "step5_extraction_result.png")

print("README visuals generated successfully in docs/")