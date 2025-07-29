import cv2
import numpy as np

# 이미지 불러오기
dino_img = cv2.imread('../img/dinosaur.png')
dino2_img = cv2.imread('../img/dinosaur1.png')
bg_img = cv2.imread('../img/background.png')

# 이미지 불러오기 확인
if dino_img is None or dino2_img is None or bg_img is None:
    print("이미지 중 하나 이상을 불러오지 못했습니다.")
    exit()

# 공룡 이미지 크기 조정 (배경에 맞게)
dino_img = cv2.resize(dino_img, (400, 300))  # 원하는 크기로 조절
dino2_img = cv2.resize(dino2_img, (300, 300))  # 필요에 따라 조정
bg_img = cv2.resize(bg_img, (960, 540))  # 배경 이미지 크기 설정

# ====== 공통 함수: 초록색 제거 후 합성 ======
def overlay_image(bg, fg_img, position, lower_green=(40, 100, 100), upper_green=(80, 255, 255)):
    x_offset, y_offset = position
    hsv = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)
    fg = cv2.bitwise_and(fg_img, fg_img, mask=mask_inv)

    rows, cols, _ = fg.shape
    roi = bg[y_offset:y_offset+rows, x_offset:x_offset+cols]
    bg_roi = cv2.bitwise_and(roi, roi, mask=mask)
    combined = cv2.add(bg_roi, fg)
    bg[y_offset:y_offset+rows, x_offset:x_offset+cols] = combined
    return bg

# ====== 공룡 1 삽입 ======
bg_img = overlay_image(bg_img, dino_img, (100, 200))

# ====== 공룡 2 (여러 마리 있는 스프라이트 이미지) 삽입 ======
bg_img = overlay_image(bg_img, dino2_img, (600, 200))  # 위치는 조정 가능

# 결과 보기
cv2.imshow('Dino + Sprite in Meadow', bg_img)
cv2.waitKey(0)
cv2.destroyAllWindows()