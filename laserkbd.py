import cv2
import numpy as np
import os

class Laserkbd:
    def __init__(self, path=None):
        self.char = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
                 'x', 'c', 'v', 'b', 'n', 'm', 'esc', 'backspace', 'space', 'enter', ',', '.']
        if path is None:
            self.configure = None
            # self.background = None
        else:
            # self.background = cv2.imread(r"{}\img-{}.png".format(path, self.char[0]), 0)
            self.configure = self.get_configure(path)
        self.char_print = ""  # 将要打印的字符串
        self.cap = cv2.VideoCapture(1)  # 打开摄像头
        self.flag_break = False  # 虚拟键盘'esc'的标志
        self.flag_out = True  # 每次正常打印的标志

    # 读取每个字符的图像，写入文件
    def get_img(self, path):
        i = 0
        while (i < len(self.char)):
            _, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # wait for ESC key to exit
                break
            elif k == ord('s'):  # wait for 's' key to save and exit
                cv2.imwrite(r"{}\img-{}.png".format(path, self.char[i]), gray)
                print("img-{}".format(self.char[i]))
                i += 1

        self.cap.release()
        cv2.destroyAllWindows()

    # 读取文件中的图像作为键盘配置
    def get_configure(self, path):
        i = os.system('cls')  # cmd清屏
        print('ready...', end='', flush=True)
        ret = {}
        for i in range(len(self.char)):
            img = cv2.imread(r"{}\img-{}.png".format(path, self.char[i]), 0)
            # img = cv2.absdiff(img, self.background)

            sumi, sumj, count = 0, 0, 0
            for row in range(480):
                for column in range(40, 320):
                    if img.item((row, column)) >= 50:
                        sumi = sumi + row
                        sumj = sumj + column
                        count = count + 1
            ret[self.char[i]] = (sumi // count, sumj // count)
        # print(ret)
        # print('ok')
        return ret

    # 匹配光斑
    def match(self, gray):
        sumi, sumj, count = 0, 0, 0
        for row in range(480):
            for column in range(40, 320):
                # 出现光斑
                if gray.item((row, column)) >= 50:
                    sumi += row
                    sumj += column
                    count += 1

        # 确定光斑中心
        if (count >= 50) and self.flag_out:
            dict_compare = {}
            result = (sumi // count, sumj // count)

            for k, (x, y) in self.configure.items():  # 将result与字典中的按键比较，结果存在dict_compare字典中
                dict_compare[k] = np.array([result[0], x]).var() + np.array([result[1], y]).var()
                # dict_compare[k] = abs(result[0] - x) + abs(result[1] - y)

            # 找出差值最小的，即为结果
            min_compare = min(dict_compare.values())
            for k, v in dict_compare.items():
                if v == min_compare:
                    # print(k,':',result,",min:",min_compare)
                    if k == 'esc':
                        self.flag_break = True
                        break
                    elif k == 'enter':
                        self.char_print += '\n'
                    elif k == 'backspace':
                        self.char_print = self.char_print[0:-1]
                    elif k == 'space':
                        self.char_print += ' '
                    else:
                        self.char_print += k
                    self.flag_out = False
                    i = os.system('cls')  # cmd清屏
                    print(self.char_print, end='', flush=True)

        elif count < 50 and self.flag_out == False:  # 没有光斑且上一帧存在光斑，即手指离开虚拟键盘后，才能继续正常打印，防止输出重复字母
            self.flag_out = True


    def work(self):
        i = os.system('cls')  # cmd清屏
        while (True):
            _, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转为灰度图
            # cv2.imshow('frame', gray)  # 显示图像
            # gray = cv2.absdiff(gray, self.background)
            # cv2.imshow('frame', gray)  # 显示图像

            keyboard = cv2.waitKey(1) & 0xFF  # 每次1毫秒间隔等待'笔记本'键盘输入
            if keyboard == 27:  # 'esc'退出
                break
            else:
                self.match(gray)
                if self.flag_break == True:  # 虚拟键盘'esc'时退出
                    break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    readpath = r"D:\program file\pycahrm\pyfile\laserkbd\fengshu" # 图像读取的目录
    Laserkbd(path=readpath).work()

    # writepath = r"D:\program file\pycahrm\pyfile\laserkbd\fengshu" # 图像存储的目录
    # Laserkbd().get_img(writepath)