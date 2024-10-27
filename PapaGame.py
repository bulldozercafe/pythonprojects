import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga-like Shooting Game")
clock = pygame.time.Clock()

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 플레이어 설정
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5

# 적 설정
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
enemy_speed = 2
enemies = []
for _ in range(1000):  # 적 5개 생성
    enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemy_y = random.randint(-150, -50)
    enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))

# 총알 설정
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
bullets = []
bullet_speed = 7

# 메인 게임 루프
running = True
while running:
    screen.fill(BLACK)

    # 종료 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 플레이어 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player_x += player_speed
    if keys[pygame.K_SPACE]:  # 스페이스바로 총알 발사
        bullet_rect = pygame.Rect(player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player_y, BULLET_WIDTH, BULLET_HEIGHT)
        bullets.append(bullet_rect)

    # 총알 이동
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:  # 화면 밖으로 나간 총알 삭제
            bullets.remove(bullet)

    # 적 이동
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > SCREEN_HEIGHT:  # 적이 화면 아래로 내려가면 다시 위로
            enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemy.y = random.randint(-150, -50)

    # 적과 총알 충돌 처리
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break  # 한 총알로 여러 적을 없앨 수 없도록 함

    # 화면에 플레이어 그리기
    pygame.draw.rect(screen, WHITE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # 화면에 적 그리기
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    # 화면에 총알 그리기
    for bullet in bullets:
        pygame.draw.rect(screen, (0, 255, 0), bullet)

    for _ in range(1):  # 적 5개 생성
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy_y = random.randint(-150, -50)
        enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 종료 처리
pygame.quit()
sys.exit()
