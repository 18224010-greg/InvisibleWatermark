# Invisible Watermarking

This project implements **invisible image watermarking** using the **DCT (Discrete Cosine Transform)** method.  
The watermark is embedded into a face image and then tested against JPEG compression using several **Quality Factor (QF)** values.

## Identity

- **Name:** Gregory William Sutjipto
- **NIM:** 18224010

---

## Objective

The objectives of this project are:

1. To embed an invisible watermark into a personal face image.
2. To test watermark robustness after JPEG compression.
3. To determine the lowest acceptable QF where the watermark can still be extracted successfully.

---

## Method Overview

The method used in this project is **DCT-based invisible watermarking**.

The general process is:

1. Load and resize the input image.
2. Generate a binary watermark.
3. Split the image into 8×8 blocks.
4. Apply DCT to selected blocks.
5. Modify selected DCT coefficients to embed watermark bits.
6. Compress the watermarked image using JPEG.
7. Extract the watermark and evaluate the result using BER and Accuracy.

---

# Step-by-Step Results

## Step 1 — Image Preprocessing

The input face image is loaded, converted into RGB, resized to **512×512**, and prepared for block-based processing.  
The image is divided into **8×8 blocks** because DCT watermarking is performed block by block.

![Step 1 - Image Preprocessing](docs/step1_preprocessing.png)

---

## Step 2 — Binary Watermark Generation

The watermark is generated as a **32×32 binary image** containing the text `WM`.  
This watermark is converted into a bit pattern consisting of `0` and `1`.

![Step 2 - Binary Watermark](docs/step2_watermark.png)

---

## Step 3 — DCT-Based Embedding

The image is converted into the YCrCb color space, and the watermark is embedded into the **Y channel**.  
For each selected 8×8 block, two DCT coefficients are modified to represent watermark bit `0` or `1`.

![Step 3 - DCT Embedding](docs/step3_dct_embedding.png)

The embedding rule is:

- If the watermark bit is `1`, one DCT coefficient is made larger than the other.
- If the watermark bit is `0`, the coefficient order is reversed.

This allows the watermark to be hidden in the frequency domain without being directly visible.

---

## Step 4 — Before and After Watermarking Comparison

The comparison below shows the image before watermarking, after watermarking, and after JPEG compression with **QF 100**.

![Step 4 - Before After QF100](docs/step4_before_after_qf100.png)

From the comparison, the watermarked image still looks visually similar to the original image.  
The difference map shows that the changes exist, but they are not clearly visible to the human eye.

---

## Step 5 — Watermark Extraction

After JPEG compression, the watermark is extracted from the compressed image.  
The extracted watermark is then compared with the original watermark.

![Step 5 - Extraction Result](docs/step5_extraction_result.png)

The extraction is tested on several QF values to see how compression affects watermark robustness.

---

# JPEG Compression Test

The tested QF values are:

`100, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5`

A lower QF means stronger JPEG compression.  
Stronger compression may damage the embedded watermark information.

The watermark is considered **OK** if:

1. `QF >= 30`
2. `BER <= 0.30`

---

## Quantitative Evaluation

| QF | BER | Accuracy | Status |
|---:|---:|---:|---|
| 100 | 0.000000 | 1.000000 | OK |
| 95 | 0.000000 | 1.000000 | OK |
| 90 | 0.000000 | 1.000000 | OK |
| 80 | 0.000000 | 1.000000 | OK |
| 70 | 0.000000 | 1.000000 | OK |
| 60 | 0.000000 | 1.000000 | OK |
| 50 | 0.000000 | 1.000000 | OK |
| 40 | 0.000000 | 1.000000 | OK |
| 30 | 0.045898 | 0.954102 | OK |
| 20 | 0.185547 | 0.814453 | GAGAL |
| 10 | 0.144531 | 0.855469 | GAGAL |
| 5 | 0.089844 | 0.910156 | GAGAL |

---

## BER Visualization

The following graph shows the relationship between JPEG QF and BER.

![BER Graph](hasil_watermarking/grafik_BER_vs_QF.png)

Based on the graph and table, the watermark can still be extracted successfully up to **QF 30**.

---

# Sample Output Files

## Original Image

![Original Image](hasil_watermarking/01_foto_asli.png)

## Original Watermark

![Original Watermark](hasil_watermarking/02_watermark_asli.png)

## Watermarked Image

![Watermarked Image](hasil_watermarking/03_foto_berwatermark_lossless.png)

## Watermarked Image after JPEG QF 100

![Watermarked QF 100](hasil_watermarking/foto_berwatermark_QF_100.jpg)

## Extracted Watermark at QF 100

![Extracted QF 100](hasil_watermarking/watermark_ekstrak_QF_100.png)

## Extracted Watermark at QF 30

![Extracted QF 30](hasil_watermarking/watermark_ekstrak_QF_30.png)

## Extracted Watermark at QF 5

![Extracted QF 5](hasil_watermarking/watermark_ekstrak_QF_5.png)

---

# Conclusion

The DCT-based invisible watermarking method successfully embeds a watermark into the input face image.

Based on the evaluation:

- QF 100 to QF 40 gives perfect extraction results with BER = 0.
- QF 30 still gives acceptable extraction with BER = 0.045898 and Accuracy = 0.954102.
- QF below 30 is considered failed based on the experiment criteria.

Therefore, the minimum acceptable JPEG Quality Factor in this experiment is:

## **QF = 30**

---

# Repository Contents

| File / Folder | Description |
|---|---|
| `watermarking.py` | Main watermarking program |
| `generate_readme_visuals.py` | Script to generate README visualization images |
| `hasil_watermarking/` | Output images and evaluation results |
| `docs/` | Step-by-step visual explanation images |
| `README.md` | Project documentation |