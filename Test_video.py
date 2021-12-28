import PySimpleGUI as sg
import cv2 as cv
import numpy as np




def main():
    imageTypes={'Type1':[1080,1920],
            'Type2': [1080,1080],
            'Type3': [1080,566],
            'Type4': [1080,1350],
            'Type5': [1200,630],
            'Type6': [851,315],
            'Type7': [640,480]}

    filename = sg.popup_get_file('Search File')
    if filename is None:
        return
    vidFile = cv.VideoCapture(filename)
    num_frames = vidFile.get(cv.CAP_PROP_FRAME_COUNT)
    fps = vidFile.get(cv.CAP_PROP_FPS)

    sg.theme('Black')

    layout = [[sg.Slider(range=(0, num_frames),size=(60, 10), orientation='h', key='-slider-'),sg.Button('Exit', size=(7, 1), font='Helvetica 14')],
              [sg.Image(filename='',size=(100,10), key='-image1-'), sg.Image(filename='',size=(100,10), key='-image2-')],
              [sg.Image(filename='',size=(50,10), key='-image3-'), sg.Image(filename='',size=(50,10), key='-image4-')]]

              #[sg.Slider(range=(0, num_frames),size=(60, 10), orientation='h', key='-slider-')]]

    window = sg.Window('Frame', layout, no_titlebar=False, location=(0, 0),size=(1920,1080))

    image_elem1 = window['-image1-']
    image_elem2 = window['-image2-']
    image_elem3 = window['-image3-']
    image_elem4 = window['-image4-']
    slider_elem = window['-slider-']

    cur_frame = 0
    while vidFile.isOpened():
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            break
        ret, frame = vidFile.read()
        if not ret:  
            break
        if int(values['-slider-']) != cur_frame-1:
            cur_frame = int(values['-slider-'])
            vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)
        slider_elem.update(cur_frame)
        cur_frame += 1
        frameResize = cv.resize(frame,(imageTypes['Type6'][0],imageTypes['Type6'][1]))
        imgTransform = cv.cvtColor(frameResize, cv.COLOR_RGB2GRAY)
        kernel = np.ones((5,5),np.float32)/25
        imgTransform2D = cv.filter2D(imgTransform,-1,kernel) 
        imgTransformLap = cv.Canny(imgTransform2D,100,200)
        imgbytes = cv.imencode('.png', frameResize)[1].tobytes()  
        imgbytes2 = cv.imencode('.png', imgTransform)[1].tobytes() 
        imgbytes3 = cv.imencode('.png', imgTransform2D)[1].tobytes() 
        imgbytes4 = cv.imencode('.png', imgTransformLap)[1].tobytes() 
        image_elem1.update(data=imgbytes)
        image_elem2.update(data=imgbytes2)
        image_elem3.update(data=imgbytes3)
        image_elem4.update(data=imgbytes4)        

main()