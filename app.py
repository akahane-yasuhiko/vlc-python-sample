'''
静止画を表示
"q"を押されたら動画を表示
escか"q"を押されるor動画終了で元の静止画を表示
"q"を押されたら終了
'''

# 動画再生用
import vlc

# 動画再生中にキー入力を検知する用 pygameやmsvcrtでは検出できなかった。ブロックされている？？
# import pygame
# import sys
# import msvcrt
from pynput import keyboard

# 静止画表示用
import cv2

import time

class movie_player:
    def __init__(self):
        '''
        動画再生できる状態まで作っておく
        '''
        # VLCインスタンスを作成 x=1920にするとウィンドウがセカンドディスプレイに位置するようにする
        # self.instance = vlc.Instance('--video-x=1920', '--video-y=10')
        self.instance = vlc.Instance()
        # メディアプレーヤーを作成
        self.player = self.instance.media_player_new()
        # 再生するメディアを指定
        self.media = self.instance.media_new(".\\sample.mp4")
        # メディアプレーヤーにメディアを設定
        self.player.set_media(self.media)
        # 全画面表示にする
        self.player.set_fullscreen(True)
        
    def play_movie(self):
        '''
        initで作られたplayerで動画再生する
        '''
        try:
            # メディア再生を開始
            self.player.play()
            
            # 同じ"q"で中断するので1秒待たないと
            time.sleep(1)
            
            # キーボード監視のコールバック関数
            def on_key_release(key):
                # escは普通に比較できるが'q'はエンコードの問題で普通に比較すると一致しないためstrに変換してから比較する
                if (key == keyboard.Key.esc or str(key) == "'q'")\
                    or (self.player.get_state() == vlc.State.Ended):
                    # "q"キーが押下された場合、メディアプレーヤーを停止
                    self.player.stop()
                    return False

            # キーボード監視を開始
            with keyboard.Listener(on_release=on_key_release) as listener:
                listener.join()
        finally:
            self.player.release()
            self.instance.release()
            


def show_image():
    img = cv2.imread('.\\sample.png')
    cv2.namedWindow('screen', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('screen', img)
    while True:
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

def close_image():
    cv2.destroyAllWindows()

# 動画再生のインスタンス取得
p = movie_player()

# qが押されるまでイメージ表示
show_image()

# 動画を再生
p.play_movie()

# 動画再生が終わるとイメージが表示されるので、qが押されるまで待つ
while True:
    if cv2.waitKey(100) & 0xFF == ord("q"):
        break

close_image()
