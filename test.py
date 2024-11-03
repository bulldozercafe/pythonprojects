import pygame
import random
import time

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 900, 950
background = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shooting Game')

# 플레이어 설정
player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5

# 적 설정
enemy_width = 50
enemy_height = 50
enemies = []
enemy_spawn_time = 3000  # 3000ms = 3초
last_spawn_time = pygame.time.get_ticks()

# 메인 루프
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += player_speed

    # 적 생성
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= enemy_spawn_time:
        enemy_x = random.randint(0, width - enemy_width)  # 적의 x 좌표 랜덤 설정
        enemies.append([enemy_x, 0])  # 적을 리스트에 추가 (x좌표, y좌표)
        last_spawn_time = current_time  # 마지막 생성 시간 업데이트

    # 배경 그리기
    background.fill((0, 0, 255))  # 파란색 배경

    # 플레이어 사각형 그리기
    pygame.draw.rect(background, (255, 255, 255), (player_x, player_y, player_width, player_height))

    # 적 그리기 및 이동
    for enemy in enemies:
        enemy[1] += 2  # 적을 아래로 이동 (y좌표 증가)
        pygame.draw.rect(background, (255, 0, 0), (enemy[0], enemy[1], enemy_width, enemy_height))  # 적 그리기

    # 화면 업데이트
    pygame.display.update()

    # FPS 조정
    pygame.time.Clock().tick(60)

# Pygame 종료
pygame.quit()
