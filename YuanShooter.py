import pygame
import random
import cv2
import time

# 게임 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 760, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yuan Shooter")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 중력/바운스
GRAVITY = 0.5
BOUNCE = -0.95  # 튀어 오를 때 반동 정도

# OpenCV 초기 설정
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 이미지 로드
explosion_image = pygame.image.load("explosion.png")  # 폭발 애니메이션 이미지
enemy_ufo_image = pygame.image.load("ufo_game_enemy.png").convert_alpha()
background_sky_image = pygame.image.load("apt_sky.png").convert_alpha()
background_building_image = pygame.image.load("apt_building.png").convert_alpha()
intro_image = pygame.image.load("intro.png").convert_alpha()

# 폭발 스프라이트 프래임 추출
explosion_width = explosion_image.get_width() // 8   # 가로 프레임 수
explosion_height = explosion_image.get_height() // 4 # 세로 프레임 수
explosion_frames = []

for row in range(4):      # 세로 4행
    for col in range(8):   # 가로 8열
        frame = explosion_image.subsurface(
            pygame.Rect(col * explosion_width, row * explosion_height, explosion_width, explosion_height)
        )
        explosion_frames.append(frame)


# 배경 위치 초기화
sky_x = -((background_sky_image.get_width() - WIDTH) / 2)
building_x = -((background_building_image.get_width() - WIDTH) / 2)
building_speed = 0.5  # 건물 배경 이동 속도

enemy_id = 0

def GetEnemyId():
    global enemy_id
    enemy_id += 1
    return enemy_id


# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))  # 플레이어 이미지를 단순하게 사각형으로 설정
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.lives = 5
        self.character_speed = 15

        # 중립 위치 설정
        self.center_threshold = 50  # 얼굴이 중앙에서 벗어났을 때 이동하도록 설정하는 임계값

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.character_speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.character_speed

        # OpenCV로 웹캠 이미지 가져오기
        ret, frame_org = cap.read()
        frame = cv2.flip(frame_org, 1)
        if not ret:
            print("웹캠을 열 수 없습니다.")

        # 얼굴 검출
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        face_image_surface = None  # 얼굴 이미지 초기화

        # 얼굴 위치 기반 캐릭터 이동
        for (x, y, w, h) in faces:
            face_center_x = x + w // 2
            screen_center_x = frame.shape[1] // 2

            global building_x  # 전역 변수 building_x에 접근
            # 얼굴 위치가 화면 중앙을 기준으로 좌우로 얼마나 이동했는지 확인
            if face_center_x < screen_center_x - self.center_threshold:
                self.rect.x -= self.character_speed  # 왼쪽 이동
                if self.rect.x > 0:
                    building_x += building_speed
            elif face_center_x > screen_center_x + self.center_threshold:
                self.rect.x += self.character_speed  # 오른쪽 이동
                if self.rect.x < screen.get_width() - self.rect.width:
                    building_x -= building_speed

            # 캐릭터가 화면을 벗어나지 않도록 제한
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > screen.get_width() - self.rect.width:
                self.rect.x = screen.get_width() - self.rect.width

            # 얼굴 이미지를 pygame Surface로 변환
            face_roi = frame[y:y + h, x:x + w]  # 얼굴 영역 추출
            face_roi = cv2.resize(face_roi, (self.rect.width, self.rect.height))  # 캐릭터 크기에 맞게 리사이즈
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)  # OpenCV의 BGR을 RGB로 변환

            # 얼굴 이미지를 -90도 회전
            face_roi = cv2.rotate(face_roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
            face_roi = cv2.flip(face_roi, 0)
            face_image_surface = pygame.surfarray.make_surface(face_roi)  # pygame Surface로 변환

            # 얼굴 영역 그리기 (OpenCV 창에서 확인용)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Pygame 캐릭터 그리기 (얼굴 이미지를 캐릭터로 표시)
        if face_image_surface:
            self.image = face_image_surface

        # OpenCV 창에 웹캠 이미지 출력
        cv2.imshow("Webcam", frame)


# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = GetEnemyId()
        self.image = pygame.transform.scale(enemy_ufo_image, (100, 100))
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(-100, -40)))
        self.BALL_SPEED_X = 5
        self.BALL_RADIUS = 20

        # 공 초기 위치 및 속도
        self.ball_speed_x = self.BALL_SPEED_X
        self.ball_speed_y = 0  # 초기 Y 속도는 0으로 설정

        # 폭발 애니메이션 관련 속성
        self.is_exploding = False
        self.explosion_frame = 0
        self.explosion_speed = 1  # 폭발 애니메이션 속도

    def update(self):
        if self.is_exploding:
            # 폭발 애니메이션 중일 때 해당 프레임 업데이트
            if self.explosion_frame < len(explosion_frames):
                self.image = explosion_frames[int(self.explosion_frame)]
                self.explosion_frame += self.explosion_speed
            else:
                super().kill() # 폭발 애니메이션이 끝나면 제거
        else:
            # 일반 상태에서 적이 할 행동 (예: 움직임)
            # 중력 적용
            self.ball_speed_y += GRAVITY
            self.rect.x += self.ball_speed_x
            self.rect.y += self.ball_speed_y

            # 좌우 경계 처리
            if self.rect.x <= self.BALL_RADIUS or self.rect.x >= screen.get_width() - self.BALL_RADIUS:
                self.ball_speed_x = -self.ball_speed_x  # 좌우 방향 반전

            # 바닥에 닿았을 때 튀어 오르기 처리
            if self.rect.y >= screen.get_height() - self.BALL_RADIUS:
                self.rect.y = screen.get_height() - self.BALL_RADIUS  # 땅 위에 위치 고정
                self.ball_speed_y *= BOUNCE  # 반동

            if self.rect.top > HEIGHT:
                super().kill()  # 화면 밖으로 나가면 제거

    def kill(self):
        # 추가 작업 실행 (예: 사운드 재생, 점수 추가)
        print(f"{self.id} Enemy has been destroyed!")
        if (self.is_exploding == False):
            self.is_exploding = True  # 총알에 맞으면 폭발 시작
            self.explosion_frame = 0

    # 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # 총알 이미지를 단순하게 사각형으로 설정
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 10  # 총알이 위로 이동
        if self.rect.bottom < 0:
            super().kill()  # 화면 밖으로 나가면 제거


# 게임 루프
def game_loop():
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    score = 0
    bullet_time = 0  # 총알 발사 타이머
    enemy_spawn_time = 0  # 적 생성 타이머
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    return  # 게임 오버 후 다시 시작

        if not game_over:
            current_time = pygame.time.get_ticks()

            if current_time - bullet_time > 1000:  # 0.5초마다 총알 발사
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                bullet_time = current_time

            if current_time - enemy_spawn_time > random.randint(5000, 10000):  # 1~3초마다 적 생성
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
                enemy_spawn_time = current_time

            all_sprites.update()

            # 충돌 처리
            if pygame.sprite.spritecollide(player, enemies, True):
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True
                    time.sleep(3)

            # 적이 총알에 맞으면 폭발 애니메이션 (스프라이트 처리 필요)
            for bullet in bullets:
                hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
                for enemy in hit_enemies:
                    score += 1
                    enemy.kill()
                    enemies.remove(enemy)

            # 게임 배경 화면 표시
            screen.fill((0, 0, 0))
            screen.blit(background_sky_image, (sky_x, 0))  # 하늘 배경 고정
            screen.blit(background_building_image, (building_x, 0))  # 건물 배경 이동
            screen.blit(background_building_image, (building_x + background_building_image.get_width(), 0))  # 건물 이미지 무한 반복

            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        else:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            time.sleep(3)
            return


# 시작 화면
def start_screen():
    font = pygame.font.Font(None, 150)
    text = font.render("Yuan Shooter", True, BLUE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    font = pygame.font.Font(None, 60)
    blinking_text = font.render("press space key to play", True, WHITE)
    blinking_text_rect = blinking_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    clock = pygame.time.Clock()
    blinking = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop()

        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(intro_image, (WIDTH, HEIGHT)), (0,0))
        screen.blit(text, text_rect)

        if blinking:
            screen.blit(blinking_text, blinking_text_rect)
        if pygame.time.get_ticks() % 1000 < 500:  # 0.5초마다 깜빡임
            screen.blit(blinking_text, blinking_text_rect)

        pygame.display.flip()
        clock.tick(60)


# 메인 실행
start_screen()
pygame.quit()
