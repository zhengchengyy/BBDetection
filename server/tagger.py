import tkinter as tk
import time
from pymongo import MongoClient


class Timer(tk.Label):
    """Label widget which can display text and bitmaps."""

    def __init__(self, master=None, cnf={}, **kw):
        self.counter = 0
        self.minute, self.second = 0, 0
        self.terminated = True
        tk.Widget.__init__(self, master, 'label', cnf, kw)

    def reset(self):
        self.minute = 0
        self.second = 0
        self.counter = 0

    def print_time(self):
        def addz(n):
            if n < 10:
                return '0' + str(n)
            else:
                return str(n)

        min = addz(self.minute)
        second = addz(self.second)
        subsecond = addz(self.counter)
        return min + ':' + second + ':' + subsecond

    def count(self):
        if not self.terminated:
            self.counter += 1
            if self.counter > 99:
                self.counter = 0
                self.second += 1
                if self.second > 59:
                    self.second = 0
                    self.minute += 1
            self.config(text=self.print_time())
            self.after(10, self.count)

    def start(self):
        self.reset()
        self.terminated = False
        self.count()

    def terminate(self):
        self.terminated = True
        self.config(text='Written successfully!')


def click():
    global timer
    global clicked
    global button, tag
    global inittime,db, collection
    if clicked:
        clicked = False
        timer.terminate()
        button.config(text='Start', bg='green')
        # Command to execute when terminating
        termtime = time.time()
        msg = {'inittime': inittime, 'termtime': termtime, 'tag': tag.get(1.0, "end-1c")}
        collection.insert_one(msg)
    else:
        clicked = True
        button.config(text='Terminate', bg='red')
        timer.start()
        # Command to execute when start
        inittime = time.time()

def click_interval(interval):
    pass

if __name__ == '__main__':
    # mongodb
    client = MongoClient()
    db = client.beaglebone
    collection = db.tags_1105
    inittime = time.time()

    root = tk.Tk()
    # text widget, the content is what should be inserted into database as a tag
    tag = tk.Text(root, height='3', width=30)
    tag.pack()

    # timer widget
    timer = Timer(root, fg='black', bg='#CCCCCC', width=30)
    timer.pack()

    # button
    clicked = False
    button = tk.Button(root, text='Start', fg='white', bg='green', command=click, width='30')
    button.pack()
    root.mainloop()


# 每个动作的时间间隔不超过1s，每个动作30s
# 静止：没人静止(still)、有人静止(still_people)
# 床上有没有人：上床(get_up)、下床(go_to_bed)

# 大动作：转身、翻身(turn_over)、腿部伸展(legs_stretch)、手部伸展(hands_stretch)
# 中等动作：腿部抖动(legs_tremble)、手部抖动(hands_tremble)、身体抖动(body_tremble)
# 小动作：头部微小移动(head_move)、腿部微小移动(legs_move)、手部微小移动(hands_move)
# 其它动作：手部抬起(hands_rising)、踢踹(kick)
# zheng