import numpy as np
from PIL import Image

from extract_watermark import extract_watermark

# Thay đổi một pixel trong hình ảnh đã nhúng
img = Image.open('watermarked_image.png')
img_array = np.array(img)
img_array[0, 0, 0] = 255  # Thay đổi pixel đầu tiên
modified_img = Image.fromarray(img_array)
modified_img.save('modified_image.png')

# Trích xuất watermark từ hình ảnh đã thay đổi
extracted_modified = extract_watermark('modified_image.png', len('SecretMessage'))
print(f"Watermark trích xuất sau khi thay đổi: {extracted_modified}")