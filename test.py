import numpy as np
from PIL import Image
import os

from embed_watermark import embed_watermark
from extract_watermark import extract_and_verify, print_verification_result

# Tạo thư mục output nếu chưa tồn tại
if not os.path.exists('embed_image'):
    os.makedirs('embed_image')

# Nhúng watermark vào ảnh gốc
original_image = 'image/image1.jpg'
watermarked_image = 'embed_image/watermarked_image.png'
embed_watermark(original_image, watermarked_image)

print("\nKiểm tra ảnh gốc đã nhúng watermark:")
result_original = extract_and_verify(watermarked_image)
print_verification_result(result_original)

# Thay đổi một pixel trong vùng ROI của ảnh đã nhúng watermark
img = Image.open(watermarked_image)
img_array = np.array(img)
height, width = img_array.shape[:2]
mid_h, mid_w = height // 2, width // 2

# Thay đổi một vùng pixels trong ROI
roi_h_start = mid_h - mid_h//4
roi_h_end = mid_h + mid_h//4
roi_w_start = mid_w - mid_w//4
roi_w_end = mid_w + mid_w//4

# Tạo một hình chữ nhật trắng trong ROI
img_array[roi_h_start:roi_h_start+50, roi_w_start:roi_w_start+50] = [255, 255, 255]

modified_img = Image.fromarray(img_array)
modified_image_path = 'embed_image/modified_image.png'
modified_img.save(modified_image_path)

print("\nKiểm tra ảnh đã bị chỉnh sửa:")
result_modified = extract_and_verify(modified_image_path)
print_verification_result(result_modified)

