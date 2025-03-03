import numpy as np
from PIL import Image

def embed_watermark(image_path, watermark, output_path):
    # Mở hình ảnh
    img = Image.open(image_path)
    img_array = np.array(img)

    # Chuyển watermark thành chuỗi bit
    watermark_bits = ''.join(format(ord(char), '08b') for char in watermark)
    watermark_length = len(watermark_bits)

    # Kiểm tra dung lượng
    if watermark_length > img_array.size:
        raise ValueError("Watermark quá lớn so với hình ảnh")

    # Nhúng watermark vào LSB của các pixel
    flat_img = img_array.flatten()
    for i in range(watermark_length):
        pixel = flat_img[i]
        flat_img[i] = (pixel & 0xFE) | int(watermark_bits[i])

    # Chuyển về hình dạng ban đầu và lưu hình ảnh
    watermarked_img_array = flat_img.reshape(img_array.shape)
    watermarked_img = Image.fromarray(watermarked_img_array)
    watermarked_img.save(output_path)
    print(f"Watermark đã được nhúng và lưu tại {output_path}")

# Ví dụ sử dụng
embed_watermark('input_image.png', 'SecretMessage', 'watermarked_image.png')