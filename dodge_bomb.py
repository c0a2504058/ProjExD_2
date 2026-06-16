import random
import os
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def cheak_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRect or 爆弾Rect 
    戻り値：判定結果タプル（True：画面内／False：画面外）
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    gameover_rct = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(gameover_rct, (0,0,0), pg.Rect(0,0,WIDTH,HEIGHT))
    gameover_rct.set_alpha(190)
    gameover_font = pg.font.Font(None,80)
    txt = gameover_font.render("Game Over",True, (255, 255, 255))
    gameover_rct.blit(txt, [420, 300])

    kk8_img = pg.image.load("fig/8.png")
    gameover_rct.blit(kk8_img, [370, 300])
    gameover_rct.blit(kk8_img, [730, 300])

    screen.blit(gameover_rct,[0,0])
    pg.display.update()
    time.sleep(5)
    
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]: 
    kk_img = pg.image.load("fig/3.png") 
    kk_dict = { 
        (0,  0): pg.transform.rotozoom(kk_img, 0, 1),
        (+5, 0): pg.transform.rotozoom(kk_img, 0, 1),
        (+5, -5): pg.transform.rotozoom(kk_img, 45, 1),
        ( 0, -5): pg.transform.rotozoom(kk_img, 90, 1),
        } 
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx,vy = +5 ,+5

    clock = pg.time.Clock()
    tmr = 0
    kk_imgs = get_kk_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
         #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
         #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #   sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #   sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)

        kk_img = kk_imgs[tuple(sum_mv)]

        if cheak_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        bb_rct.move_ip(vx,vy)

        yoko, tate = cheak_bound(bb_rct)

        if not yoko:
            vx *= -1

        if not tate:
            vy *= -1
            
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
