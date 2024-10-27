import pygame
import random

# 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("경주하는 말들")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 말 클래스 정의
class Horse(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += random.randint(1, 3)  # 말들의 속도 조정

# 말들 생성
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
horses = pygame.sprite.Group()
for i, color in enumerate(colors):
    horse = Horse(50, 100 * (i + 1), color)
    horses.add(horse)

# 메인 게임 루프
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경색 채우기
    screen.fill(WHITE)

    # 말들 업데이트
    horses.update()

    # 말들 그리기
    horses.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 조절
    clock.tick(30)  # 초당 30프레임으로 설정

    # 승리 조건 확인
    for horse in horses:
        if horse.rect.x >= screen_width - 50:
            print(f"말 {colors[horses.sprites().index(horse)]}가 우승했습니다!")
            running = False

pygame.quit()
