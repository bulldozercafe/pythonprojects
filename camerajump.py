import pygame
import cv2
import numpy as np
import threading

# 기본 설정
pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jump Game")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 게임 요소
player_size = 50
player_pos = [100, height - player_size]
gravity = 0.8
player_vel_y = 0
is_jumping = False

obstacle_width, obstacle_height = 40, 80
obstacle_pos = [width, height - obstacle_height]
obstacle_speed = 10

# Load sprite sheet and define animation parameters
sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
sprite_width = 64  # 각 프레임의 가로 길이
sprite_height = 128  # 각 프레임의 세로 길이
num_frames = 5  # 애니메이션에 포함된 프레임 수

# 애니메이션 프레임 인덱스
frame_index = 0

# 배경음악
pygame.mixer.music.load("Stereo Madness.mp3")
pygame.mixer.music.play(-1)

# 카메라 설정
cap = cv2.VideoCapture(0)
jump_detected = False


def detect_jump():
    global jump_detected
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # 간단한 점프 감지 예제: 중간 위치와 상단 위치의 차이 분석
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        middle_area = gray[height // 2 - 50:height // 2 + 50, width // 2 - 50:width // 2 + 50]
        top_area = gray[height // 4 - 50:height // 4 + 50, width // 2 - 50:width // 2 + 50]

        middle_brightness = np.mean(middle_area)
        top_brightness = np.mean(top_area)

        if top_brightness > middle_brightness + 20:  # 기준을 조절
            jump_detected = True
        else:
            jump_detected = False

        # 카메라 화면 표시
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# 점프 감지 스레드
jump_thread = threading.Thread(target=detect_jump)
jump_thread.start()

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 플레이어 점프 처리
    if jump_detected and not is_jumping:
        player_vel_y = -15
        is_jumping = True
        jump_detected = False

    # 중력 적용
    player_vel_y += gravity
    player_pos[1] += player_vel_y

    # 바닥에 닿으면 점프 종료
    if player_pos[1] >= height - player_size:
        player_pos[1] = height - player_size
        is_jumping = False

    # 장애물 이동
    obstacle_pos[0] -= obstacle_speed
    if obstacle_pos[0] < 0:
        obstacle_pos[0] = width

    # 현재 프레임을 스프라이트 시트에서 잘라내기
    body_frame_rect = pygame.Rect(frame_index * sprite_width, 0, sprite_width, sprite_height)
    body_frame = sprite_sheet.subsurface(body_frame_rect)
    screen.blit(body_frame, (270, 200))
    frame_index = (frame_index + 1) % num_frames

    # 플레이어와 장애물 그리기
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, BLACK, (obstacle_pos[0], obstacle_pos[1], obstacle_width, obstacle_height))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(30)

# 종료 처리
cap.release()
cv2.destroyAllWindows()
pygame.quit()
