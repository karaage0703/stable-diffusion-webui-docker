#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
import shutil
import os
import docker
import subprocess

"""
Demo program that displays a webcam using OpenCV

Reference: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py 
"""


def main():

    sg.theme('Black')

    # get docker info
    client = docker.from_env()
    container_name = client.containers.list()[0].name

    live_img_path = '../../../output/ai_zoo/live.png'

    # define the window layout
    layout = [[sg.Text('AI どうぶつえん', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image'), sg.Image(filename='', key='image2')],
              [sg.Button('Clear', size=(10, 1), font='Helvetica 14'),
               sg.Button('Shutter', size=(10, 1), font='Helvetica 14'),
               sg.Button('Convert', size=(10, 1), font='Helvetica 14'),
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


        is_file = os.path.isfile('./live.png')
        if is_file:
            live_img = cv2.imread('./live.png')
            imgbytes_2 = cv2.imencode('.png', live_img)[1].tobytes()
        else:
            blank_img = np.full((512, 512), 255)
            imgbytes_2 = cv2.imencode('.png', blank_img)[1].tobytes()
        window['image2'].update(data=imgbytes_2)

        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Clear':
            recording = True
            os.remove('./live.png')  

        elif event == 'Shutter':
            recording = False
            cv2.imwrite('./input.png', frame)

        elif event == 'Convert':
            shutil.copyfile('./input.png', '../../../cache/input.png')

            client = docker.from_env()
            container_name = client.containers.list()[0].name

            cmd = 'docker exec ' + container_name + ' python scripts/ai_zoo.py --prompt "kawaii bear" --seed -1 --init-img /cache/input.png --strength 0.7 --skip_grid'
            subprocess.run(cmd, shell=True)
            shutil.copyfile('../../../output/ai_zoo/live.png', './live.png')

main()