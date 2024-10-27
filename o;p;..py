import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)


# 공룡 클래스
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\\pic\\dino2.png");
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 70
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 0.5

    def update(self):
        if self.is_jumping:
            self.rect.y -= self.jump_speed
            self.jump_speed -= self.gravity
            if self.rect.y >= HEIGHT - 70:
                self.rect.y = HEIGHT - 70
                self.is_jumping = False
                self.jump_speed = 10

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True


# 장애물 클래스
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\\pic\\cac.png");
        #self.image = pygame.Surface((20, 50))
        #self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 70


    def update(self):
        self.rect.x -= 5
        if self.rect.x < -20:
            self.kill()


# 점수 표시 함수
def display_score(score):
    font = pygame.font.SysFont(None, 55)
    score_text = font.render(f"{score}", True, (100, 100, 100))
    screen.blit(score_text, (10, 10))


# 스프라이트 그룹
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

dino = Dino()
all_sprites.add(dino)

# 게임 루프
running = True
clock = pygame.time.Clock()

nGap = 0

score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()

    # 업데이트
    all_sprites.update()

    # 장애물 생성
    nGap += 1

    if nGap == 50:
        if random.randint(0, 100) > (100 - 50):
            obstacle = Obstacle()
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        nGap = 0


    # 충돌 감지
    if pygame.sprite.spritecollideany(dino, obstacles):
        print("Game Over!")
        print(score)
        running = False

    # 화면 그리기
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # 장애물 통과 스코어
    # for obs in obstacles:
    #    if obs.rect.x == 0:
    #        score += 1

    # 거리 스코어
    score += 1

    # 점수 표시
    display_score(int(score/5))

    pygame.display.flip()

    # 프레임 속도 조절
    clock.tick(60)

pygame.quit()