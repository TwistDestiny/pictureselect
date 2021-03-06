import shutil
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import glob
import os
from PIL import Image,ImageTk
from risize_pic import AutoScrollbar, CanvasImage,w_box,h_box
import json

def resize( w_box, h_box, pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片
  w, h = pil_image.size #获取图像的原始大小
  f1 = 1.0*w_box/w
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)

# w_box = 2200    #frame的大小
# h_box = 1000    #frame的大小
x_button1= 400
x_button2= 600
x_button3= 800
y_button = 850
list_x = w_box + 50
tips_y = 1100
class Picture(object):
    def __init__(self, init_window_name):
        self.window = init_window_name
        self.image_path = []
        self.img_num = 0
        self.num = 0
        self.welcome_path = './welcome.jpg'  # 初始化图片

    def init_window(self):
        self.window.geometry('1920x1080')
        # self.window.resizable(0, 0)  # 防止用户调整尺寸
        self.window.title("图片预览器")
        self.menubar = Menu(self.window)
        self.filemenu = Menu(self.window, tearoff=0)
        self.aboutmenu = Menu(self.window, tearoff=0)
        self.menubar.add_cascade(label='文件', menu=self.filemenu)
        self.menubar.add_cascade(label='关于', menu=self.aboutmenu)
        self.filemenu.add_command(label='打开', command=self.select_file)
        self.aboutmenu.add_command(label='版本号: 2.0')
        self.aboutmenu.add_command(label='作者: YYM')
        self.label_img = Frame(self.window,height=h_box,width=w_box,borderwidth=10,relief="ridge")

        self.label_img.grid_propagate(0)
        self.label_img.grid()
        self.label_img.place(x=10, y=10)
        # root.destroy()
        # self.welcome = Label(self.window, text='图片预览器', fg='white', bg='#126bae', font=('Arial', 12), width=34,
        #                      height=2).place(x=230, y=10)
        # self.img_open = Image.open(self.welcome_path)
        # self.img_open = resize(w_box, h_box, self.img_open)
        # self.image = ImageTk.PhotoImage(self.img_open)


        self.window.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.window.columnconfigure(0, weight=1)
        canvas = CanvasImage(self.label_img, self.welcome_path)  # create widget
        canvas.grid(row=0, column=0)  # show widget


        # self.label_img = Label(self.window, height=h_box, width=w_box, borderwidth=10, relief="ridge")
        # self.label_img.place(x=10, y=10)


        self.var_path = StringVar()

        self.path = Label(self.window,textvariable=self.var_path,
                         highlightcolor='red', font=('Arial', 12), height=1).place(x=250, y=tips_y)

        self.pre_btn = Button(self.window, text='上一张', font=('Arial', 12), fg='white', width=10, height=1,
                              command=self.pre_img, bg='#126bae', state=DISABLED)
        self.pre_btn.place(x=x_button1, y=y_button)
        self.next_btn = Button(self.window, text='下一张', font=('Arial', 12), fg='white', width=10, height=1,
                               command=self.next_img,bg='#126bae', state=DISABLED)
        self.next_btn.place(x=x_button2, y=y_button)


        self.theLB = Listbox(self.window, selectmode=BROWSE, height=20)  # height=11设置listbox组件的高度，默认是10行。
        self.theLB.pack()
        self.item = ['流线', '裂纹', '模粉坑', '重皮', '龟裂', '铁豆', '环裂', '气孔', '铸痕', '下渣', '下铁', '拔裂', '纵裂', '碎芯承口错台', '气坑']
        for item in ['流线', '裂纹', '模粉坑', '重皮', '龟裂', '铁豆', '环裂', '气孔', '铸痕', '下渣', '下铁', '拔裂', '纵裂', '碎芯承口错台', '气坑']:
            self.theLB.insert(END, item)  # END表示每插入一个都是在最后一个位置
        self.theButton = Button(self.window, text='确定', font=('Arial', 12), fg='black', width=10, height=1, command=self.save_img, state=DISABLED)
        print(str.split(str(self.var_path),"//"))
        self.theLB.place(x=list_x,y=20)
        self.theButton.place(x=x_button3,y=y_button)
        self.window.config(menu=self.menubar)
        self.window.mainloop()

    def save_img(self):
        # print("tuple")
        # print(self.theLB.curselection())
        if not os.path.exists(".\\PictureClassification\\"):
            os.mkdir(".\\PictureClassification\\")
        file_dir = ".\\PictureClassification\\"+self.item[self.theLB.curselection()[0]]+"\\"
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file_old = self.image_path[self.num]
        shutil.copy(file_old,file_dir + str.split(file_old,"\\")[-1])



    def select_file(self):
        chose_dir = tkinter.filedialog.askdirectory()
        path = glob.glob(os.path.join(chose_dir, '*.tiff'))
        self.img_num = len(path)
        self.image_path = path
        filename = "numbers.json"
        self.num = 0

        if(os.path.exists(filename)) and self.img_num != 0:
            with open(filename) as file_obj:
                data = json.load(file_obj)
                print(data)
                print(self.image_path[0])
                if data['path'].replace('\\', '/') ==self.image_path[0].replace('\\', '/'):
                    self.num = data['index']
        if self.img_num == 0:
            tkinter.messagebox.showinfo(title='提示', message='当前文件夹文件没有图片!')
        else:
            self.var_path.set(self.image_path[self.num].replace('\\', '/'))
            # img_open = Image.open(path[0])
            # img_open = resize(w_box, h_box, img_open)
            # image = ImageTk.PhotoImage(img_open)
            #
            # self.label_img.configure(image=image)
            # self.label_img.image = image

            self.window.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
            self.window.columnconfigure(0, weight=1)
            canvas = CanvasImage(self.label_img, self.image_path[self.num])  # create widget
            canvas.grid(row=0, column=0)  # show widget

            self.next_btn['state'] = NORMAL
            self.pre_btn['state'] = NORMAL
            self.theButton['state'] = NORMAL

    def next_img(self):

        self.num += 1
        if self.num >= self.img_num:
            self.num = self.img_num - 1
            tkinter.messagebox.showinfo(title='提示', message='到头了哦！')
        while(True):
            img_open = Image.open(self.image_path[self.num])

            self.last_img = Image.open(self.image_path[self.num - 1])
            from PIL import ImageChops
            difference = ImageChops.difference(self.last_img, img_open)
            if difference.getbbox() is None:
                self.var_path.set("重复的图片！")
            else:
                self.var_path.set(self.image_path[self.num].replace('\\', '/'))
                break
            self.num += 1
            if self.num >= self.img_num:
                self.num = self.img_num - 1
                tkinter.messagebox.showinfo(title='提示', message='到头了哦！')
                break

        # img_open = resize(w_box, h_box, img_open)

        # image = ImageTk.PhotoImage(img_open)
        # self.label_img.configure(image=image)
        # self.label_img.image = image
        self.window.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.window.columnconfigure(0, weight=1)
        canvas = CanvasImage(self.label_img, self.image_path[self.num])  # create widget
        canvas.grid(row=0, column=0)  # show widget
        # self.last_img = Image.open(self.image_path[self.num - 1])
        # from PIL import ImageChops
        # difference = ImageChops.difference(self.last_img, img_open)
        # if difference.getbbox()  is None:
        #     self.var_path.set("重复的图片！")
        # else:
        #     self.var_path.set(self.image_path[self.num].replace('\\', '/'))
        self.save_i()

        # file_old = self.image_path[self.num]
        # print(str.split(file_old, "\\")[-1])

    def pre_img(self):
        self.num -= 1
        if self.num < 0:
            self.num = 0
            tkinter.messagebox.showinfo(title='提示', message='啊偶！没有图片了')
        img_open = Image.open(self.image_path[self.num])
        img_open = resize(w_box, h_box, img_open)
        self.var_path.set(self.image_path[self.num].replace('\\', '/'))
        # image = ImageTk.PhotoImage(img_open)
        # self.label_img.configure(image=image)
        # self.label_img.image = image
        self.window.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.window.columnconfigure(0, weight=1)
        canvas = CanvasImage(self.label_img, self.image_path[self.num])  # create widget
        canvas.grid(row=0, column=0)  # show widget
        self.save_i()

    def save_i(self):
        data={}
        data["path"] = self.image_path[0]
        data["index"] = self.num
        filename = "numbers.json"
        with open(filename, 'w') as file_obj:
            json.dump(data, file_obj)


if __name__ == "__main__":
    windows = Tk()
    picture = Picture(windows)
    picture.init_window()

