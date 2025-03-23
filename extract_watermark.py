import numpy as np
from PIL import Image
from utils import (
    divide_into_regions,
    calculate_hash,
    bits_to_bytes,
    bytes_to_bits
)

def extract_watermark_bits(roni1):
    """Trích xuất các bit watermark từ RONI-1"""
    # Lấy LSB từ RONI-1
    flat_roni1 = roni1.flatten()
    bits = ''.join(str(pixel & 1) for pixel in flat_roni1)
    return bits

def extract_and_verify(image_path):
    """Trích xuất và xác minh watermark từ ảnh"""
    try:
        # Đọc ảnh
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Chia ảnh thành ROI và RONI
        roi, ronis, roi_coords = divide_into_regions(img_array)
        
        # Trích xuất watermark từ RONI-1
        extracted_bits = extract_watermark_bits(ronis[0])
        
        try:
            # Chuyển chuỗi bit thành bytes và sau đó thành string
            watermark_bytes = bits_to_bytes(extracted_bits)
            watermark_str = watermark_bytes.decode('utf-8', errors='ignore')
            
            # Hiển thị watermark string đã trích xuất
            print("\nWatermark đã trích xuất (secretkey):")
            try:
                parts = watermark_str.split('|')
                if len(parts) >= 1:
                    print(f"Hash ROI trích xuất: {parts[0]}")
                if len(parts) >= 9:
                    print(f"Hash các vùng RONI trích xuất: {parts[1][:10]}... đến {parts[8][:10]}...")
                print(f"Tổng độ dài watermark trích xuất: {len(watermark_str)} ký tự")
                print(f"Số phần tách được: {len(parts)}")
            except Exception as e:
                print(f"Lỗi khi hiển thị chi tiết watermark: {e}")
                print(f"Nội dung watermark thô: {watermark_str[:50]}...")
            
            # Tách thành các thành phần
            parts = watermark_str.split('|')
            if len(parts) < 9:  # Phải có ít nhất hash ROI + 8 hash RONI
                raise ValueError(f"Watermark không hợp lệ, chỉ có {len(parts)} phần")
                
            h_roi_ext = parts[0]
            h_ronis_ext = parts[1:9]
            
            # Tính hash mới cho ROI và RONI
            h_roi_new = calculate_hash(roi)
            h_ronis_new = [calculate_hash(roni) for roni in ronis]
            
            # So sánh hashes
            roi_modified = h_roi_ext != h_roi_new
            roni_modifications = [(i+1, h_ext != h_new) 
                                for i, (h_ext, h_new) in enumerate(zip(h_ronis_ext, h_ronis_new))]
            modified_ronis = [i for i, modified in roni_modifications if modified]
            
            # In thông tin hashes để debug
            print("\nKiểm tra hash ROI:")
            print(f"- Hash ROI từ watermark: {h_roi_ext}")
            print(f"- Hash ROI hiện tại:     {h_roi_new}")
            
            return {
                'roi_modified': roi_modified,
                'modified_ronis': modified_ronis,
                'original_roi': roi,
                'roi_coords': roi_coords
            }
        except Exception as e:
            print(f"Lỗi khi phân tích watermark: {e}")
            return {
                'roi_modified': True,
                'modified_ronis': list(range(1, 9)),
                'original_roi': roi,
                'roi_coords': roi_coords
            }
    except Exception as e:
        print(f"Lỗi khi đọc ảnh hoặc trích xuất watermark: {e}")
        return {
            'roi_modified': True,
            'modified_ronis': list(range(1, 9)),
            'original_roi': None,
            'roi_coords': None
        }

def print_verification_result(result):
    """In kết quả xác minh"""
    print("\nKết quả xác minh:")
    if result['roi_modified']:
        print("✗ ROI đã bị chỉnh sửa!")
    else:
        print("✓ ROI không bị chỉnh sửa")
    
    if result['modified_ronis']:
        print(f"✗ Các vùng RONI sau đã bị chỉnh sửa: {result['modified_ronis']}")
    else:
        print("✓ Không có vùng RONI nào bị chỉnh sửa")
        
    # Lưu ROI hiện tại để so sánh
    if result['original_roi'] is not None:
        roi_img = Image.fromarray(result['original_roi'])
        roi_img.save('embed_image/current_roi.png')