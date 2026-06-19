import cv2
import os
import numpy as np

for data in ['train', 'val', 'test']:
  mask_dir = 'v1coco-segmentation-maskLebels/{}/masks'.format(data)  # โฟลเดอร์ที่เป็นภาพ mask ปัจจุบัน
  output_dir = 'v1coco-segmentation-maskLebels/{}/labels'.format(data) # โฟลเดอร์ที่จะเซฟไฟล์ .txt

  os.makedirs(output_dir, exist_ok=True)

  for mask_name in os.listdir(mask_dir):
    if not mask_name.endswith('.jpg') and not mask_name.endswith('.png'):
      continue
        
    mask_path = os.path.join(mask_dir, mask_name)
    
    # อ่านไฟล์แบบดั้งเดิม (Unchanged) เพื่อรักษาค่าพิกเซลจริงไว้
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    
    # ปรับตรงนี้: ถ้าค่าพิกเซลมากกว่า 0 ให้เปลี่ยนเป็น 255 (สีขาว) ให้หมดเพื่อให้หาเจอ
    # หรือถ้า Mask ของคุณเป็นแบบคลาสแยก ให้ลูปตามจำนวนคลาสได้เลย
    _, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)

    thresh = thresh.astype(np.uint8)
    
    # หา Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    h, w = mask.shape[:2]
    txt_name = os.path.splitext(mask_name)[0] + '.txt'
    
    with open(os.path.join(output_dir, txt_name), 'w') as f:
      for contour in contours:
        if len(contour) < 3:
          continue
        
        segmentation = []
        for point in contour:
          x, y = point[0]
          segmentation.append(f"{x / w:.6f} {y / h:.6f}")
      
        # ระบุ Class ID (ปรับตามความเหมาะสม)
        class_id = 0 
        line = f"{class_id} " + " ".join(segmentation) + "\n"
        f.write(line)