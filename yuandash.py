import pygame
import cv2
import sys
import random
import numpy as np

# 게임 초기 설정
pygame.init()
display_width = 1280
display_height = 720
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Yuan Dash")
clock = pygame.time.Clock()

# 배경음악 로드
pygame.mixer.music.load("Stereo Madness.mp3")

# 스프라이트 시트와 캐릭터 애니메이션 설정
sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
sprite_width, sprite_height = 90, 120  # 각 프레임의 크기
run_frames = 8  # 달리기 애니메이션 프레임 수
jump_frames = 8  # 점프 애니메이션 프레임 수

# OpenCV 카메라 초기화
cap = cv2.VideoCapture(0)

# 게임 변수 초기화
game_started = False
character_x, character_y = 100, 400
is_jumping = False
jump_velocity = 15
gravity = 1
current_frame = 0
collision_count = 0

# 시작 화면 텍스트
font = pygame.font.Font(None, 74)
logo_text = font.render("Yuan Dash", True, (255, 0, 0))
start_text = pygame.font.Font(None, 36).render("Press SPACE BAR to start", True, (255, 255, 255))
game_over_text = font.render("Game Over", True, (255, 0, 0))

# 장애물 및 플랫폼 설정
obstacle_timer = 0
platform_timer = 0
obstacles = []
platforms = []


def create_obstacle():
    return pygame.Rect(800, 450, 50, 50)


def create_platform():
    return pygame.Rect(800, random.randint(300, 500), 100, 20)


# 메인 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                    pygame.mixer.music.play(-1)  # 배경음악 반복 재생
                    collision_count = 0
                elif not is_jumping:
                    is_jumping = True

    # 게임 시작 전 로고 화면
    if not game_started:
        screen.fill((0, 0, 0))
        screen.blit(logo_text, (250, 200))
        screen.blit(start_text, (250, 300))
        pygame.display.flip()
        continue

    # OpenCV로 웹캠에서 영상 받아오기
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Webcam", frame)  # 옆에 웹캠 화면 표시

        # 웹캠 앞에서 점프 탐지 (간단한 움직임 감지로 시뮬레이션)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        movement_detected = np.mean(gray) > 150  # 밝기 값으로 점프 감지
        if movement_detected and not is_jumping:
            is_jumping = True

    # 화면 초기화
    screen.fill((135, 206, 235))  # 하늘색 배경

    # 장애물 생성 및 이동
    if obstacle_timer > random.randint(50, 150):
        obstacles.append(create_obstacle())
        obstacle_timer = 0

    for obstacle in obstacles:
        obstacle.x -= 5
        if obstacle.colliderect(pygame.Rect(character_x, character_y, sprite_width, sprite_height)):
            collision_count += 1
            obstacles.remove(obstacle)
        elif obstacle.x < -50:
            obstacles.remove(obstacle)
        pygame.draw.rect(screen, (255, 0, 0), obstacle)  # 장애물 표시

    # 플랫폼 생성 및 이동
    if platform_timer > random.randint(100, 200):
        platforms.append(create_platform())
        platform_timer = 0

    for platform in platforms:
        platform.x -= 3
        if platform.x < -100:
            platforms.remove(platform)
        pygame.draw.rect(screen, (0, 255, 0), platform)  # 플랫폼 표시

    # 캐릭터 애니메이션: 점프 / 달리기
    if is_jumping:
        frame_rect = pygame.Rect(40 + (current_frame % jump_frames) * sprite_width + (current_frame % jump_frames) * 80, 200, sprite_width, sprite_height)
        character_y -= jump_velocity
        jump_velocity -= gravity
        if jump_velocity < -15:
            is_jumping = False
            jump_velocity = 15
    else:
        #frame_rect = pygame.Rect((current_frame % run_frames) * sprite_width, 0, sprite_width, sprite_height)
        frame_rect = pygame.Rect(40 + (current_frame % run_frames) * sprite_width + (current_frame % jump_frames) * 80, 30, sprite_width, sprite_height)

    # 캐릭터가 플랫폼에 있을 때
    on_platform = any(
        pygame.Rect(character_x, character_y + sprite_height, sprite_width, 1).colliderect(p) for p in platforms)
    if not on_platform and not is_jumping:
        character_y += 5  # 낙하 속도

    character_frame = sprite_sheet.subsurface(frame_rect)
    screen.blit(character_frame, (character_x, character_y))

    # 애니메이션 프레임 업데이트
    current_frame += 1
    obstacle_timer += 1
    platform_timer += 1

    # 충돌 카운트가 10이 되면 게임 오버
    if collision_count >= 10:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (250, 300))
        pygame.display.flip()
        pygame.time.delay(1000)
        game_started = False  # 게임 시작 화면으로 돌아감

    pygame.display.flip()
    clock.tick(30)

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
