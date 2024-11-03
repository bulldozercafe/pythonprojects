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

# ===================플레이어 체력, 점수=================
player_health = 5
score = 0
coll_frame = 0
# ======================================================


def enemies_list(enemies, frame):
        x = random.randint(1,2)
        if frame % 1 == 0:
            if x==1:
                x_pos = 0   # -->
                x_vel = 5
                y_vel = 0
            else:
                x_pos = 850 # <--                                   0      1      2      3       4
                x_vel = -10
                y_vel = 0
            enemies.append([x_pos, 200, x_vel,y_vel , 3])    # [x_pos, y_pos, x_vel, y_vel,  health]


def gunshots(x_pos, y_pos, bullet, frame):
    if frame % 1 == 0:
            bullet.append([x_pos + 20, y_pos])    # [x_pos, y_pos]




while play:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            play = False

    # 키로 동작
    '''
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
    '''


    # ===============마우스 위치 가져오기 ================
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > 850:
        mouse_x = 850

    x_pos = mouse_x # 마우스 위치로 플레이어 이동
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

        # 폰트 설정 (폰트 이름, 크기)
        font = pygame.font.Font(None, 36)  # 기본 폰트 사용, 크기 36
        text = font.render(str(en[4]), True, (255, 255, 255))  # 흰색 글씨
        background.blit(text, (en[0], en[1], 50, 50))
    

    # BULLET================================================================================
    for e in enemies:
        for b in bullet:
            if b[1] < -50:
                bullet.remove(b)
                continue

            enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기
            bullet_rect = pygame.Rect(b[0], b[1], 10, 20)     # 총알 사각형 데이터 만들기

            # 충돌 확인
            if bullet_rect.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리                                
                # bullet.remove(b)
                pygame.draw.rect(background, ('yellow'), (e[0], e[1], 50, 50), 5) # 번쩍 효과
                e[4] -= 1  # 적 체력 1 깎기
                if(e[4] < 1): # 적 체력이 1보다 작으면 삭제하기
                    if e in enemies:
                        enemies.remove(e)
                        score += 1    # 적이 죽으면 점수 + 1

    player_rect = pygame.Rect(x_pos, y_pos, 50, 50)
    for e in enemies:
        enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기
        

        # PLAYER============================================================================
        # 충돌 확인
        if frame > coll_frame + 100: 
            if player_rect.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리
                pygame.draw.rect(background, ('yellow'), (x_pos, y_pos, 50, 50), 10) # 번쩍 효과
                coll_frame = frame
                player_health -= 1



    font = pygame.font.Font(None, 60)  # 기본 폰트 사용, 크기 36
    
    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))  # 흰색 글씨
    background.blit(score_text, (0, 0, 100, 100)) # 화면에 그리기

    health_text = font.render('Health : ' + str(player_health), True, (255, 255, 255))  # 흰색 글씨
    background.blit(health_text, (650, 0, 100, 100)) # 화면에 그리기
            

    
    

    # UPDATE frame
    frame +=1
    if frame % 60 == 0:
        second +=1

    pygame.time.Clock().tick(60)
    pygame.display.update()  

pygame.quit()