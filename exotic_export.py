import pyautogui as pg
import pygetwindow as gw
import keyboard as kb
import pynput
import time
import cv2
import numpy as np
window = gw.getWindowsWithTitle("Grand Theft Auto V")
if window:
    w = window[0]
    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
else:
    print("no game detected, quit")
    exit()
def LocateTarget(target_name,retry=100):
    # 定位用函数
    global w
    global keyboard
    for i in range(retry):
        try:
            location = pg.locateOnScreen(image=f"locate/{target_name}.png",confidence=0.8,region=(w.left,w.top,w.width,w.height))
            pg.center(location)
            return location
        except:
            if target_name == "online":
                keyboard.press(pynput.keyboard.Key.esc)
                keyboard.release(pynput.keyboard.Key.esc)
            elif target_name == "job":
                try:
                    ltmp = pg.locateOnScreen(image=f"locate/enter_job.png",confidence=0.8,region=(w.left,w.top,w.width,w.height))
                    return 0
                except:
                    pass
            elif target_name != "job_screen" :
                pg.mouseDown(button="left")
                pg.mouseUp(button="left")
            # print(f"image {target_name} not found, retry in 300ms")
            time.sleep(0.3)
    return None
    
def click(target):
    # 点击用函数（左键）
    target_location = LocateTarget(f"{target}")
    if target_location is None:
        print("stucked, try to figure out y")
        exit()
    pg.moveTo(target_location)
    for i in range(2):
        pg.mouseDown(button="left")
        pg.mouseUp(button="left")
        if target == "job":
            return
    
def EnterJobs():
    # 用于进入团队生存页面，后续选择点位
    global keyboard
    time.sleep(1)
    keyboard.press(pynput.keyboard.Key.esc)
    keyboard.release(pynput.keyboard.Key.esc)
    time.sleep(0.5)
    img_name = ["online","job","enter_job","star","team"]
    for i in range(5):
        click(img_name[i])
        

def SearchBlueSpot(f):
    # 利用cv2的inRange函数寻找蓝点
    global w
    # 截取屏幕图像做后续处理
    pg.screenshot(imageFilename="screen.png",region=(w.left,w.top,w.width,w.height))
    img = cv2.imread("screen.png")
    # 截取地图进行识别，此处为窗口模式1904x1001，只要识别到整个小地图即可（手动修改，但是感觉可以自动化，只要检测到防弹衣那个条即可）
    x,y,w,h=80,830,280,180
    roi = img[y:y+h,x:x+w]
    hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    if f == 0:
        # 检测地图是否出现（通过防弹衣的条，注意不要有装备防弹衣）
        lower_blue=np.array([100,100,50])
    else:
        # 检测蓝点
        lower_blue=np.array([100,100,200])
    upper_blue=np.array([120,255,255])

    msk = cv2.inRange(hsv_roi,lower_blue,upper_blue)
    if cv2.countNonZero(msk)>0:
        return 1
    else:
        return 0

def Searching():
    global keyboard
    global mouse
    global w
    for i in range(0,53):
        # 首先进入差事界面
        print(i)
        EnterJobs()
        if i >= 27:
            for j in range(53-i):
                # 使用滚轮上选择差事
                time.sleep(0.2)
                mouse.scroll(0, 1)
        else:
            for j in range(i):
                # 使用滚轮下选择差事
                time.sleep(0.2)
                mouse.scroll(0, -1)

        #进入差事
        time.sleep(0.3)
        keyboard.press(pynput.keyboard.Key.enter)
        keyboard.release(pynput.keyboard.Key.enter)
        time.sleep(0.4)
        keyboard.press(pynput.keyboard.Key.enter)
        keyboard.release(pynput.keyboard.Key.enter)

        # # 方案一：检测差事界面
        # # 检测是否进入差事界面
        # job_screen_location = LocateTarget("job_screen")
        # if job_screen_location is not None:
        #     # 进入差事则退出
        #     pg.mouseDown(button="right")
        #     pg.mouseUp(button="right")
        #     time.sleep(0.5)
        #     keyboard.press(pynput.keyboard.Key.enter)
        #     keyboard.release(pynput.keyboard.Key.enter)
        
        #方案二：检测退出界面
        while True:
            pg.mouseDown(button="right")
            pg.mouseUp(button="right")
            try:
                location = pg.locateOnScreen(image="locate/job_screen2.png",confidence=0.8,region=(w.left,w.top,w.width,w.height))
                keyboard.press(pynput.keyboard.Key.enter)
                keyboard.release(pynput.keyboard.Key.enter)
                break
            except:
                pass

        # 退出后查找是否存在蓝点
        while not SearchBlueSpot(0):
            #首先判断是否进入地图界面
            # print("cant see the map, waiting")
            time.sleep(3)
        time.sleep(8)
        location = SearchBlueSpot(1)
        if location:
            print("find car!")
            break
        


if __name__ == "__main__":
    
    kb.add_hotkey('ctrl+e',Searching)
    kb.wait("u")
    # Searching()
