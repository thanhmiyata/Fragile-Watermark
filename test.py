import numpy as np
from PIL import Image

from embed_watermark import embed_watermark
from extract_watermark import extract_watermark

# Nhúng watermark vào hình ảnh gốc
original_image = 'image/image1.jpg'
watermark = 'SecretMessage'
watermarked_image = 'embed_image/watermarked_image.png'
embed_watermark(original_image, watermark, watermarked_image)

# Thay đổi một pixel trong hình ảnh đã nhúng
img = Image.open(watermarked_image)
img_array = np.array(img)
img_array[0, 0, 0] = 255  # Thay đổi pixel đầu tiên
modified_img = Image.fromarray(img_array)
modified_image_path = 'embed_image/modified_image.png'
modified_img.save(modified_image_path)

# Trích xuất watermark từ hình ảnh đã thay đổi
extracted_modified = extract_watermark(modified_image_path, len(watermark))
print(f"Watermark trích xuất sau khi thay đổi: {extracted_modified}")

# Trích xuất watermark từ hình ảnh chưa thay đổi để so sánh
extracted_original = extract_watermark(watermarked_image, len(watermark))
print(f"Watermark trích xuất từ ảnh gốc: {extracted_original}")

