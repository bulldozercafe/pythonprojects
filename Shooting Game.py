import pygame
import random

pygame.init()

background = pygame.display.set_mode((900, 950))
pygame.display.set_caption('Shoot!')

x_pos = 450
y_pos = 870

to_x = 0
to_y = 0

right = False
left = False

play = True

enemies = []
bullet = []

frame = 0
second = 0

gravity = 0.5

# ===================플레이어 체력, 점수=====================
player_health = 5
score = 0
# ======================================================


def enemies_list(enemies, frame):
        x = random.randint(1,2)
        if frame % 600 == 0:
            if x==1:
                x_pos = 0   # -->
                x_vel = 10
                y_vel = 0
            else:
                x_pos = 850 # <--                                   0      1      2      3       4
                x_vel = -10
                y_vel = 0
            enemies.append([x_pos, 200, x_vel,y_vel , 3])    # [x_pos, y_pos, x_vel, y_vel,  health]


def gunshots(x_pos, y_pos, bullet, frame):
    if frame % 20 == 0:
            bullet.append([x_pos + 20, y_pos])    # [x_pos, y_pos]




while play:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            play = False

    # 키로 동작
    if event.type == pygame.KEYDOWN:  
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            left = False
            right = True
            to_x = 10
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            right = False
            left = True
            to_x = -10
    else:
        right = False
        left = False
        to_x = 0

    
    x_pos += to_x
    if x_pos < 0:  # 왼쪽 경계
        x_pos = 0
    elif x_pos > 850:  # 오른쪽 경계 (900 - 50)
        x_pos = 850




    # ===============마우스 위치 가져오기 ================
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x_pos = mouse_x
    # ===================================================

    



    # 화면에 그리기 시작
    background.fill('blue')


    # 총알 생성
    gunshots(x_pos, y_pos, bullet, frame)
    
    # 총알 그리기
    for gun in bullet:
        gun[1] -= 20
        pygame.draw.rect(background, ('yellow'), (gun[0], gun[1], 10, 20))


    # 플레이어 그리기
    pygame.draw.rect(background, ('white'), (x_pos, y_pos, 50, 50))


    # 적 새로 만들기
    enemies_list(enemies, frame)

    # 적 그리기
    for en in enemies:        
        # X속도
        if en[0] > 850 or en[0] < 0:
            en[2] = -en[2]        
        
        # Y속도
        if en[1] > 850:
            en[3] = -en[3] - 0.5
        
        en[3] += gravity
           
        # X위치 변경
        en[0] += en[2]
        # Y위치 변경
        en[1] += en[3]

        pygame.draw.rect(background, ('red'), (en[0], en[1], 50, 50))

        # ========================== 적 체력 표시하기 ====================
        # 폰트 설정 (폰트 이름, 크기)
        font = pygame.font.Font(None, 36)  # 기본 폰트 사용, 크기 36
        text = font.render(str(en[4]), True, (255, 255, 255))  # 흰색 글씨
        background.blit(text, (en[0], en[1], 50, 50))
        # ================================================================

    

    # ===========적이랑 총알이 만났는지 확인하고 삭제하기================
    for e in enemies:
        for b in bullet:
            enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기
            bullet_rect = pygame.Rect(b[0], b[1], 10, 20)     # 총알 사각형 데이터 만들기

            # 충돌 확인
            if bullet_rect.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리                
                bullet.remove(b)
                e[4] -= 1  # 적 체력 1 깎기
                if(e[4] < 1): # 적 체력이 1보다 작으면 삭제하기
                    enemies.remove(e)
                    score += 1    # 적이 죽으면 점수 + 1
    # =================================================================

    # ===========적이랑 플레이어랑 만났는지 확인하기  ================
    player_rect = pygame.Rect(x_pos, y_pos, 50, 50)
    for e in enemies:
        enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기
        
        # 충돌 확인
        if player_rect.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리
            print("으악!!")
            player_health -= 1  # (문제점) 1프레임마다 계속 깎여서 한방에 많이 깎임. 충돌하면 일정시간 동안 무적으로 처리해주어야함
    # =================================================================

    # ========================== 점수, 플레이어 체력 표시하기 ====================
    font = pygame.font.Font(None, 60)  # 기본 폰트 사용, 크기 36
    
    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))  # 흰색 글씨
    background.blit(score_text, (0, 0, 100, 100))

    health_text = font.render('Health : ' + str(player_health), True, (255, 255, 255))  # 흰색 글씨
    background.blit(health_text, (650, 0, 100, 100))
    # ================================================================
            

    
    

    # UPDATE frame
    frame +=1
    if frame % 60 == 0:
        second +=1

    pygame.time.Clock().tick(60)
    pygame.display.update()  

pygame.quit()