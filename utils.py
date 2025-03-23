import numpy as np
import hashlib
import pickle
import base64
import zlib

def divide_into_regions(image):
    """Chia ảnh thành ROI và 8 vùng RONI"""
    height, width = image.shape[:2]
    mid_h, mid_w = height // 2, width // 2
    
    # ROI là vùng trung tâm nhỏ hơn của ảnh (1/4 kích thước)
    roi_h_start = mid_h - mid_h//4
    roi_h_end = mid_h + mid_h//4
    roi_w_start = mid_w - mid_w//4
    roi_w_end = mid_w + mid_w//4
    
    roi = image[roi_h_start:roi_h_end, roi_w_start:roi_w_end].copy()
    
    # Chia RONI thành 8 vùng
    ronis = []
    # RONI 1-4: Các góc
    ronis.append(image[:mid_h//2, :mid_w//2].copy())  # RONI-1: Góc trên trái
    ronis.append(image[:mid_h//2, -mid_w//2:].copy())  # RONI-2: Góc trên phải
    ronis.append(image[-mid_h//2:, :mid_w//2].copy())  # RONI-3: Góc dưới trái
    ronis.append(image[-mid_h//2:, -mid_w//2:].copy())  # RONI-4: Góc dưới phải
    
    # RONI 5-8: Các cạnh
    ronis.append(image[:mid_h//2, mid_w//2:-mid_w//2].copy())  # RONI-5: Cạnh trên
    ronis.append(image[-mid_h//2:, mid_w//2:-mid_w//2].copy())  # RONI-6: Cạnh dưới
    ronis.append(image[mid_h//2:-mid_h//2, :mid_w//2].copy())  # RONI-7: Cạnh trái
    ronis.append(image[mid_h//2:-mid_h//2, -mid_w//2:].copy())  # RONI-8: Cạnh phải
    
    return roi, ronis, (roi_h_start, roi_h_end, roi_w_start, roi_w_end)

def simple_compress(data):
    """Nén dữ liệu sử dụng zlib thay vì LZW"""
    if isinstance(data, np.ndarray):
        # Pickle và nén bằng zlib
        pickled = pickle.dumps(data)
        compressed = zlib.compress(pickled)
        return base64.b64encode(compressed).decode('ascii')
    return None

def simple_decompress(data_str):
    """Giải nén dữ liệu"""
    try:
        compressed = base64.b64decode(data_str)
        decompressed = zlib.decompress(compressed)
        return pickle.loads(decompressed)
    except Exception as e:
        print(f"Lỗi khi giải nén: {e}")
        return None

def calculate_hash(data):
    """Tính hash SHA-256 cho một vùng dữ liệu"""
    if isinstance(data, np.ndarray):
        # Chỉ hash dữ liệu và shape
        data_bytes = data.tobytes()
        shape_str = str(data.shape).encode()
        return hashlib.sha256(data_bytes + shape_str).hexdigest()
    elif isinstance(data, str):
        return hashlib.sha256(data.encode()).hexdigest()
    else:
        return hashlib.sha256(data).hexdigest()

def bits_to_bytes(bits):
    """Chuyển chuỗi bit thành bytes"""
    # Đảm bảo độ dài bits là bội số của 8
    padding = 8 - (len(bits) % 8) if len(bits) % 8 != 0 else 0
    padded_bits = bits + '0' * padding
    
    return bytes(int(padded_bits[i:i+8], 2) for i in range(0, len(padded_bits), 8))

def bytes_to_bits(bytes_data):
    """Chuyển bytes thành chuỗi bit"""
    return ''.join(format(b, '08b') for b in bytes_data) 