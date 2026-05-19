import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path

INPUT_IMAGE = "foto_wajah.jpeg"
OUTPUT_DIR = Path("hasil_watermarking")
OUTPUT_DIR.mkdir(exist_ok=True)

IMAGE_SIZE = 512
WATERMARK_SIZE = 32
ALPHA = 18
SEED = 123

QF_LIST = [100, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5]
MIN_OK_QF = 30
FAIL_THRESHOLD_BER = 0.30

img = Image.open(INPUT_IMAGE)
img = ImageOps.exif_transpose(img)
img = img.convert("RGB")
img = img.resize((IMAGE_SIZE, IMAGE_SIZE))

original_rgb = np.array(img)
img.save(OUTPUT_DIR / "01_foto_asli.png")

wm_img = Image.new("L", (WATERMARK_SIZE, WATERMARK_SIZE), 0)
draw = ImageDraw.Draw(wm_img)
draw.text((4, 11), "greg", fill=255)

watermark = (np.array(wm_img) > 127).astype(np.uint8)

Image.fromarray((watermark * 255).astype(np.uint8)).save(
    OUTPUT_DIR / "02_watermark_asli.png"
)

def get_block_positions(h, w, n_bits, seed=123):
    positions = []

    for y in range(0, h, 8):
        for x in range(0, w, 8):
            positions.append((y, x))

    rng = np.random.default_rng(seed)
    rng.shuffle(positions)

    return positions[:n_bits]

def embed_watermark(rgb_img, wm_bits, alpha=18, seed=123):
    ycrcb = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2YCrCb)
    y_channel = ycrcb[:, :, 0].astype(np.float32)

    h, w = y_channel.shape
    bits = wm_bits.flatten()
    positions = get_block_positions(h, w, len(bits), seed)

    c1 = (4, 1)
    c2 = (3, 2)

    for bit, (row, col) in zip(bits, positions):
        block = y_channel[row:row+8, col:col+8] - 128
        dct_block = cv2.dct(block)

        avg = (dct_block[c1] + dct_block[c2]) / 2

        if bit == 1:
            dct_block[c1] = avg + alpha
            dct_block[c2] = avg - alpha
        else:
            dct_block[c1] = avg - alpha
            dct_block[c2] = avg + alpha

        idct_block = cv2.idct(dct_block) + 128
        y_channel[row:row+8, col:col+8] = np.clip(idct_block, 0, 255)

    ycrcb[:, :, 0] = y_channel.astype(np.uint8)
    watermarked_rgb = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)

    return watermarked_rgb

def extract_watermark(rgb_img, wm_shape, seed=123):
    ycrcb = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2YCrCb)
    y_channel = ycrcb[:, :, 0].astype(np.float32)

    h, w = y_channel.shape
    n_bits = wm_shape[0] * wm_shape[1]
    positions = get_block_positions(h, w, n_bits, seed)

    c1 = (4, 1)
    c2 = (3, 2)

    extracted_bits = []

    for row, col in positions:
        block = y_channel[row:row+8, col:col+8] - 128
        dct_block = cv2.dct(block)

        bit = 1 if dct_block[c1] > dct_block[c2] else 0
        extracted_bits.append(bit)

    extracted = np.array(extracted_bits, dtype=np.uint8).reshape(wm_shape)

    return extracted

watermarked_rgb = embed_watermark(original_rgb, watermark, ALPHA, SEED)

Image.fromarray(watermarked_rgb).save(
    OUTPUT_DIR / "03_foto_berwatermark_lossless.png"
)

extracted_lossless = extract_watermark(watermarked_rgb, watermark.shape, SEED)

Image.fromarray((extracted_lossless * 255).astype(np.uint8)).save(
    OUTPUT_DIR / "04_watermark_ekstrak_lossless.png"
)

lossless_ber = np.mean(extracted_lossless != watermark)

results = []

for qf in QF_LIST:
    jpeg_path = OUTPUT_DIR / f"foto_berwatermark_QF_{qf}.jpg"
    extracted_path = OUTPUT_DIR / f"watermark_ekstrak_QF_{qf}.png"

    Image.fromarray(watermarked_rgb).save(jpeg_path, quality=qf)

    compressed_rgb = np.array(Image.open(jpeg_path).convert("RGB"))
    compressed_rgb = np.array(
        Image.fromarray(compressed_rgb).resize((IMAGE_SIZE, IMAGE_SIZE))
    )

    extracted = extract_watermark(compressed_rgb, watermark.shape, SEED)

    ber = np.mean(extracted != watermark)
    accuracy = 1 - ber

    if qf >= MIN_OK_QF and ber <= FAIL_THRESHOLD_BER:
        status = "OK"
    else:
        status = "GAGAL"

    Image.fromarray((extracted * 255).astype(np.uint8)).save(extracted_path)

    results.append({
        "QF": qf,
        "BER": ber,
        "Accuracy": accuracy,
        "Status": status
    })

df = pd.DataFrame(results)
df.to_csv(OUTPUT_DIR / "hasil_evaluasi_QF.csv", index=False)

print("BER tanpa kompresi:", lossless_ber)
print(df)

ok_df = df[df["Status"] == "OK"]

if len(ok_df) > 0:
    batas_ok = ok_df["QF"].min()
    print("Watermark masih dianggap OK sampai QF:", batas_ok)
else:
    print("Tidak ada QF yang memenuhi status OK.")

plt.figure()
plt.plot(df["QF"], df["BER"], marker="o")
plt.axvline(x=30, linestyle="--")
plt.xlabel("JPEG Quality Factor (QF)")
plt.ylabel("Bit Error Rate (BER)")
plt.title("Evaluasi Watermark terhadap Kompresi JPEG")
plt.gca().invert_xaxis()
plt.grid(True)
plt.savefig(OUTPUT_DIR / "grafik_BER_vs_QF.png", dpi=200)
plt.close()