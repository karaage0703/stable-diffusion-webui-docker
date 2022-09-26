#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np

"""
Demo program that displays a webcam using OpenCV

Reference: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py 
"""


def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image'), sg.Image(filename='', key='image2')],
              [sg.Button('Save', size=(10, 1), font='Helvetica 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = True

    while True:
        event, values = window.read(timeout=20)

        if recording:
            ret, frame = cap.read()
            frame = cv2.resize(frame, dsize=(512, 512))
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['image'].update(data=imgbytes)

        blank_img = np.full((512, 512), 255)
        imgbytes_2 = cv2.imencode('.png', blank_img)[1].tobytes()
        window['image2'].update(data=imgbytes_2)

        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Save':
            recording = False
            cv2.imwrite('./input.png', frame)

main()