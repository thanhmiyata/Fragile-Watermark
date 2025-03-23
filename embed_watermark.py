import numpy as np
from PIL import Image
from utils import (
    divide_into_regions,
    calculate_hash,
    bits_to_bytes,
    bytes_to_bits
)

def create_fragile_watermark(roi, ronis):
    """Tạo fragile watermark từ ROI và các vùng RONI"""
    # Tính hash cho ROI và các vùng RONI
    h_roi = calculate_hash(roi)
    h_ronis = [calculate_hash(roni) for roni in ronis]
    
    # Kết hợp thành watermark
    # Format: [Hash ROI][Hash RONI 1-8]
    watermark_str = h_roi + "|" + "|".join(h_ronis)
    
    # Hiển thị watermark string đã tạo
    print("\nWatermark đã tạo (secretkey):")
    print(f"Hash ROI: {h_roi}")
    print(f"Hash các vùng RONI: {h_ronis[0][:10]}... đến {h_ronis[7][:10]}...")
    print(f"Tổng độ dài watermark: {len(watermark_str)} ký tự")
    
    # Mã hóa thành chuỗi bit
    watermark_bits = bytes_to_bits(watermark_str.encode('utf-8'))
    return watermark_bits

def embed_watermark(image_path, output_path):
    """Nhúng fragile watermark vào ảnh"""
    # Đọc ảnh
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Chia ảnh thành ROI và RONI
        roi, ronis, roi_coords = divide_into_regions(img_array)
        
        # Tạo fragile watermark
        watermark = create_fragile_watermark(roi, ronis)
        watermark_length = len(watermark)
        
        # Kiểm tra dung lượng
        available_space = ronis[0].size  # Chỉ sử dụng RONI-1
        if watermark_length > available_space:
            print(f"Cảnh báo: Watermark ({watermark_length} bits) lớn hơn không gian RONI-1 ({available_space} bits)")
            print(f"Sẽ chỉ nhúng {available_space} bits đầu tiên")
            watermark = watermark[:available_space]
        
        # Nhúng watermark vào RONI-1
        watermark_bits = list(watermark)
        flat_roni1 = ronis[0].flatten()
        for i in range(min(len(flat_roni1), len(watermark_bits))):
            flat_roni1[i] = (flat_roni1[i] & 0xFE) | int(watermark_bits[i])
        ronis[0] = flat_roni1.reshape(ronis[0].shape)
        
        # Ghép lại các vùng thành ảnh hoàn chỉnh
        height, width = img_array.shape[:2]
        mid_h, mid_w = height // 2, width // 2
        
        # Gán lại vùng RONI-1
        img_array[:mid_h//2, :mid_w//2] = ronis[0]  # RONI-1
        
        # Lưu ảnh đã nhúng watermark
        watermarked_img = Image.fromarray(img_array)
        watermarked_img.save(output_path)
        print(f"Đã nhúng watermark và lưu tại {output_path}")
        
        # Lưu thông tin ROI để debug
        roi_img = Image.fromarray(roi)
        roi_img.save('embed_image/original_roi_debug.png')
        
        return True
    except Exception as e:
        print(f"Lỗi khi nhúng watermark: {e}")
        return False