import numpy as np
from PIL import Image

def extract_watermark(image_path, watermark_length):
    # Mở hình ảnh đã nhúng watermark
    img = Image.open(image_path)
    img_array = np.array(img)

    # Trích xuất LSB từ các pixel
    flat_img = img_array.flatten()
    extracted_bits = ''
    for i in range(watermark_length * 8):  # Mỗi ký tự là 8 bit
        extracted_bits += str(flat_img[i] & 1)

    # Chuyển chuỗi bit thành ký tự
    watermark = ''
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i:i+8]
        watermark += chr(int(byte, 2))

    return watermark

# Ví dụ sử dụng
extracted = extract_watermark('watermarked_image.png', len('SecretMessage'))
print(f"Watermark trích xuất: {extracted}")