import pygame
import cv2
import sys
import numpy as np

# Pygame 초기 설정
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Character Control with Webcam Face")
clock = pygame.time.Clock()

# 색상 및 캐릭터 설정
WHITE = (255, 255, 255)
character = pygame.Rect(300, 400, 50, 50)  # 캐릭터 초기 위치와 크기
character_speed = 5

# OpenCV 초기 설정
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 중립 위치 설정
center_threshold = 50  # 얼굴이 중앙에서 벗어났을 때 이동하도록 설정하는 임계값

# 메인 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # OpenCV로 웹캠 이미지 가져오기
    ret, frame = cap.read()
    if not ret:
        print("웹캠을 열 수 없습니다.")
        break

    # 얼굴 검출
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    face_image_surface = None  # 얼굴 이미지 초기화

    # 얼굴 위치 기반 캐릭터 이동
    for (x, y, w, h) in faces:
        face_center_x = x + w // 2
        screen_center_x = frame.shape[1] // 2

        # 얼굴 위치가 화면 중앙을 기준으로 좌우로 얼마나 이동했는지 확인
        if face_center_x < screen_center_x - center_threshold:
            character.x -= character_speed  # 왼쪽 이동
        elif face_center_x > screen_center_x + center_threshold:
            character.x += character_speed  # 오른쪽 이동

        # 캐릭터가 화면을 벗어나지 않도록 제한
        if character.x < 0:
            character.x = 0
        elif character.x > screen.get_width() - character.width:
            character.x = screen.get_width() - character.width

        # 얼굴 이미지를 pygame Surface로 변환
        face_roi = frame[y:y + h, x:x + w]  # 얼굴 영역 추출
        face_roi = cv2.resize(face_roi, (character.width, character.height))  # 캐릭터 크기에 맞게 리사이즈
        face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)  # OpenCV의 BGR을 RGB로 변환

        # 얼굴 이미지를 -90도 회전
        face_roi = cv2.rotate(face_roi, cv2.ROTATE_90_COUNTERCLOCKWISE)

        face_image_surface = pygame.surfarray.make_surface(face_roi)  # pygame Surface로 변환

        # 얼굴 영역 그리기 (OpenCV 창에서 확인용)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Pygame 캐릭터 그리기 (얼굴 이미지를 캐릭터로 표시)
    if face_image_surface:
        screen.blit(face_image_surface, character)

    # OpenCV 창에 웹캠 이미지 출력
    cv2.imshow("Webcam", frame)

    # Pygame 업데이트
    pygame.display.flip()
    clock.tick(30)

    # 종료 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # OpenCV 종료 키 처리 (ESC 누르면 종료)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 종료 처리
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
