#coding：utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
br = webdriver.Firefox()
# serid = '663bfec0360de33fc122b0c2d8a17927_483d41d86201486eb3cee1fca4369907'
# sersign = '41f9ea92fb363394e5d9030868a7f04c'
serid = '999c04371f5d9aa62704963c11333784_033fa9e6b7224847b0bc791bcd0158a1'
sersign = '9ec1512c74d16435675b5faa34354db6'
from PIL import Image
from PIL import ImageEnhance,ImageFilter
import numpy as np
import matplotlib.pyplot as plt
#im = Image.open('img.jpg')
#im = ImageEnhance.Contrast(im)
#im = im.enhance(0.3) #对比度降低 变暗

def pic_add(im1,im,posx,show=0):
    # 原图像，小图像，叠加x
    # 0 黑 1 白
    img1=np.array(im1.convert('L'))
    img=np.array(im.convert('L'))
    rows1,cols1=img1.shape
    rows,cols=img.shape
    if cols+posx > cols1:
        cols = cols1-posx
    
    for i in range(rows):
        for j in range(cols):
            if (img[i,j]<=128):
                img[i,j]=0
            else:
                img[i,j]=1
                
    for i in range(rows1):
        for j in range(cols1):
            if (img1[i,j]<=128):
                img1[i,j]=0
            else:
                img1[i,j]=1
    
    img1 = img_del_parts(img1,rows1,cols1)
    for i in range(rows):
        for j in range(cols):
            img1[i,j+posx] = img1[i,j+posx] if img1[i,j+posx] > img[i,j] else img[i,j]         
  
    if show:
        print(img1.sum())            
        plt.figure("lena")
        plt.imshow(img1,cmap='gray')
        plt.axis('off')
        plt.show()
    return img1.sum()

def pic_to_2(im,show=0):
    img=np.array(im.convert('L'))
    rows,cols=img.shape
    for i in range(rows):
        for j in range(cols):
            if (img[i,j]<=128):
                img[i,j]=0
            else:
                img[i,j]=1
    img = img_del_parts(img,rows,cols)
    if show:
        print(img.sum())
        plt.figure("lena")
        plt.imshow(img,cmap='gray')
        plt.axis('off')
        plt.show()
    return img.sum()

def img_del_parts(img, rows, cols):
    for i in range(cols-4):
        if img[:,i:i+4].sum() > 20 :  # 30 
            img[:,i:i+4] = 0
    for i in range(rows):
        if img[i,:].sum() > 25 :      # 40 # 30--%27
            img[i,:] = 0
    return img
    
def img_check_corp(im,show=0):
    img=np.array(im.convert('L'))
    rows,cols=img.shape
    for i in range(rows):
        for j in range(cols):
            if (img[i,j]<=50):
                img[i,j]=0
            else:
                img[i,j]=1
    trange=[]
    for i in range(rows):
        tsum = img[i,:].sum()
        if tsum==60:
            continue
        if tsum > 5:
            trange.append(i)
    if show:
        print(img.sum())
        plt.figure("lena")
        plt.imshow(img,cmap='gray')
        plt.axis('off')
        plt.show()
    return (min(trange)-8,max(trange)+8)
    
def pic_get_loc():    
    im = Image.open('img.png').convert('RGB')
    # cropsize = im.getbbox() #(左上右下)到左上角距离
    # im = ImageEnhance.Contrast(im)
    # im = im.enhance(0.5) #对比度降低 变暗 
    # im = im.crop(cropsize).filter(ImageFilter.FIND_EDGES)
    im = im.filter(ImageFilter.FIND_EDGES)
    corpmm = img_check_corp(im)
    # im = Image.open('img.png').convert('RGB')
    im = im.crop([0,corpmm[0],im.width,corpmm[1]]).filter(ImageFilter.FIND_EDGES)
    # im.show()

    im1 = Image.open('img1.png').convert('RGB')
    # im1 = im1.crop([0,cropsize[1],im1.width,cropsize[3]]).filter(ImageFilter.FIND_EDGES)
    im1 = im1.crop([0,corpmm[0],im1.width,corpmm[1]]).filter(ImageFilter.FIND_EDGES)
    # im1.show()
    im1_num = pic_to_2(im1)

    new_im_num = []
    for i in range(0,im1.width-im.width,5):
        ret = pic_add(im1,im,i)
        new_im_num.append(ret)
    #     new_im = Image.new('RGB', (im1.width,im1.height))
    #     new_im.paste(im1,(0,0))
    #     new_im.paste(im,(i,0))
    #     ret = pic_to_2(new_im)
    #     new_im_num.append(ret)
    #     new_im.show()
    # print(im.width,im1.width)
    idxret = []
    white_cnt = [ abs(int(i)-int(im1_num)) for i in new_im_num ]
    idx = white_cnt.index(min(white_cnt))
    idxret.append(idx*5)
    pic_add(im1,im,idx*5)#,show=1)
    white_cnt[idx] = 10000
    idx = white_cnt.index(min(white_cnt))
    idxret.append(idx*5)
    pic_add(im1,im,idx*5)#,show=1)
    white_cnt[idx] = 10000
    idx = white_cnt.index(min(white_cnt))
    idxret.append(idx*5)
    pic_add(im1,im,idx*5)#,show=1)
    #print(idxret)
    return idxret

def page_verify(br):
    huadongshow = 0
    while huadongshow !=1:
        br.get('https://callback.ganji.com/firewall/verifycode?serialId={}&code=22&sign={}&namespace=ganji_hy_detail_pc'.format(serid,sersign))
        time.sleep(1)
        br.find_element_by_id('btnSubmit').click()
        if '向右滑动滑块填充拼图' in br.page_source:
            huadongshow = 1
            
def pic_save(br):
    jscode='''$(".dvc-captcha__puzzleImg").hide();$(".dvc-captcha__bgImg").show();'''
    br.execute_script(jscode)
    a = br.find_element_by_class_name('dvc-captcha__bgImg')
    time.sleep(1.5)
    a.screenshot('img1.png')
    jscode='''$(".dvc-captcha__puzzleImg").show();$(".dvc-captcha__bgImg").hide();'''
    br.execute_script(jscode)
    a = br.find_element_by_class_name('dvc-captcha__puzzleImg')
    time.sleep(0.5)
    a.screenshot('img.png')
    jscode='''$(".dvc-captcha__puzzleImg").show();$(".dvc-captcha__bgImg").show();'''
    br.execute_script(jscode)

# 40% 正确率    
def add_action(actions,offset):
    x=0
    while(x<=offset):
        rrand = random.randint(5,10)
        xrnd =random.randint(int(offset/6)+rrand,int(offset/4)+rrand)
        yrnd = random.randint(1,15)-10+rrand
        if offset-x < 10 or offset-x < int(offset/6)+rrand:
            xrnd =random.randint(offset-x+3,offset-x+7)        
        x=x+xrnd
        actions.move_by_offset(xrnd+random.random()*2-1,yrnd+random.random()*2-1)
    yrnd = random.randint(1,15)-10+rrand+random.random()*10-4
    actions.move_by_offset(offset-x+random.random()*2-1,yrnd+random.random()*2-1)
    return actions

def pic_verify(br,xoff):
    actions = ActionChains(br)
    bar = br.find_element_by_class_name('dvc-slider__handler')
    actions.move_to_element(bar)
    actions.click_and_hold(bar)
#     xoff = 175
#     xoff = xoff+5 if xoff>250 else xoff
    xoff = xoff
    add_action(actions,xoff)#xoff/480*280)
    actions.release()
    actions.perform()
    time.sleep(2)
    if '安全认证' not in br.page_source or '验证通过' in br.page_source:
        #print('验证成功')
        return 1
    else:
        #print('验证失败')
        return 0

runtimes = 0
successtimes = 0
while True:
    br.set_page_load_timeout(3)
    runtimes = runtimes + 1
    try:        
        page_verify(br)
        pic_save(br)
        idxret = pic_get_loc()
        for i in idxret:
            if pic_verify(br,i):
                successtimes = successtimes + 1
                break
    except Exception as e:
        print(e)
    finally:
        print('运行{}次，成功{}次，成功率{}%'.format(runtimes,successtimes,successtimes/runtimes*100))
        