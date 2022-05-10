import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from svgpath2mpl import parse_path
from model import *

shark = parse_path("""M2501 3930 c-148 -39 -253 -103 -371 -226 -115 -120 -206 -258 -266
-406 l-27 -67 -46 -6 c-338 -40 -578 -102 -941 -243 -322 -125 -775 -341 -822
-393 -45 -48 -38 -69 54 -165 229 -238 558 -454 836 -549 179 -61 231 -68 482
-66 l226 2 51 -103 c109 -219 260 -389 414 -466 150 -75 288 -94 334 -47 14
13 25 34 25 45 0 12 -39 149 -86 306 -48 157 -85 286 -83 288 2 2 104 12 227
23 l223 19 45 -56 c59 -73 152 -151 219 -184 70 -34 157 -44 208 -23 56 24 60
46 33 185 l-22 120 80 16 c79 16 81 16 96 -4 60 -82 120 -146 182 -193 164
-126 399 -196 458 -137 34 34 32 45 -46 323 -35 125 -64 229 -64 231 0 2 41
26 91 55 88 50 92 51 132 40 71 -19 204 -77 403 -175 106 -52 203 -94 216 -94
33 0 68 39 68 76 0 16 -16 128 -34 248 l-34 219 175 306 c96 168 177 320 180
337 4 24 0 37 -16 53 -43 43 -53 40 -331 -94 -296 -142 -582 -268 -652 -286
-40 -11 -58 -10 -122 5 -42 10 -77 21 -79 24 -2 4 9 95 24 202 16 107 26 207
23 222 -3 16 -15 35 -27 43 -48 34 -66 24 -292 -166 l-216 -181 -237 56 c-130
31 -284 67 -342 80 l-105 23 -3 378 c-2 373 -3 379 -24 402 -18 19 -31 23 -82
22 -34 0 -94 -9 -135 -19z m89 -445 l0 -305 -29 0 c-15 0 -53 5 -82 11 -129
25 -179 8 -179 -62 0 -60 26 -73 192 -98 170 -26 482 -92 759 -161 109 -27
207 -47 217 -43 9 3 83 62 165 129 165 139 156 140 132 -16 -20 -132 -19 -157
8 -184 29 -29 270 -91 325 -83 59 8 219 71 477 189 290 132 269 123 263 112
-3 -5 -58 -102 -122 -215 l-117 -206 26 -162 c14 -90 25 -169 25 -177 0 -11
-15 -7 -57 15 -97 48 -283 127 -366 156 -120 40 -159 38 -253 -18 -44 -25
-124 -67 -179 -92 -139 -64 -149 -70 -159 -98 -23 -63 34 -119 100 -97 20 7
37 10 38 8 2 -1 22 -70 45 -153 23 -82 44 -158 47 -168 5 -16 3 -16 -45 2
-124 47 -252 159 -314 276 -45 85 -64 92 -169 61 -46 -13 -114 -27 -153 -31
-86 -9 -110 -18 -130 -49 -16 -23 -15 -32 5 -137 11 -61 19 -114 16 -116 -16
-17 -156 110 -231 210 -46 60 -20 58 -424 22 -292 -26 -313 -33 -319 -93 -2
-17 31 -144 78 -297 45 -147 79 -270 76 -273 -12 -12 -155 70 -213 123 -102
92 -223 277 -278 428 -29 78 -37 80 -314 72 -197 -6 -248 -4 -309 9 -99 21
-241 70 -327 111 l-70 33 252 1 c249 1 252 1 279 24 35 30 37 79 5 110 -21 22
-25 22 -409 25 l-387 3 -70 54 c-38 30 -101 83 -140 118 l-70 64 143 72 c547
274 1090 453 1456 479 139 10 141 11 186 127 87 221 250 435 396 521 47 28
165 73 192 74 9 0 12 -68 12 -305z""")
shark.vertices -= shark.vertices.mean(axis=0)


# Графический интерфейс
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def show_level():
    sg.theme('Light Blue 3') 
    layout = [ [sg.Text('Выберите вид модели')],
        [sg.Button('Модель с неподвижной акулой', key='no_motion')],
        [sg.Button('Модель с движущейся акулой', key='motion')] ]
    window = sg.Window('Подводная охота', layout)
    while True:
        event, values = window.read()
        if event == 'no_motion':
            show_param_no_motion()
        if event == 'motion':
            show_param_motion()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def show_param_no_motion():
    sg.theme('Light Blue 3') 
    layout = [[sg.Text('Введите параметры модели')],
        [sg.Text('Расстояние до акулы: '), sg.Input()],
        [sg.Text('Угол до акулы: '), sg.Input()],
        [sg.Button('Ввести', key='read')] ]
    window = sg.Window('Подводная охота', layout)
    while True:
        event, values = window.read()
        if  event == 'read':
            model = Model(float(values[0]), float(values[1]), False)
            show_graph_no_motion(model)
        if event == sg.WIN_CLOSED:
            break
    window.close()
    

def show_graph_no_motion(model):
    if (model.idx == 0):
        sg.popup("Неудача", "Невозможно попасть в акулу, измените параметры")
    else:
        layout = [[sg.Text('Подводному охотнику нужно стрелять', justification='center', font='Helvetica 14')],
                [sg.Text(f'на {model.b_res:.{2}f} градусов или {model.h_res:.{2}f} метров выше акулы', justification='center', font='Helvetica 14')],
                [sg.Canvas(size=(640, 480), key='-CANVAS-')],
                [sg.Button('Отдельные траектории', key='separate'), sg.Button('Таблицы с данными', key='table')] ]
        window = sg.Window('Подводная охота', layout, finalize=True)

        canvas_elem = window['-CANVAS-']
        canvas = canvas_elem.TKCanvas
        fig, ax = plt.subplots()
        ax.grid(True)
        fig_agg = draw_figure(canvas, fig) 
        idx = 1
        while True:
            event, values = window.read(timeout=5)
            if event == sg.WIN_CLOSED:
                break
            if event == 'separate':
                window.close()
                show_separate(model)
            if event == 'table':
                window.close()
                show_tables(model)

            ax.cla()
            ax.grid(True)
            ax.scatter(model.Shark.R+1, model.Shark.H+1, s=1, alpha=0.01)
            if (idx <= model.idx):
                ax.plot(model.Harpoon.X[:idx], model.Harpoon.Y[:idx], c='g', linestyle='-')
                ax.scatter(model.Shark.R, model.Shark.H, s=3000, c='b', marker=shark)
            else:
                ax.plot(model.Harpoon.X[:idx], model.Harpoon.Y[:idx], c='g', linestyle='--')
                ax.scatter(model.Shark.R, model.Shark.H, s=3000, alpha=0.5, c='r', marker=shark)
            fig_agg.draw()
            idx += 1
            if (idx >= len(model.Harpoon.X)):
                idx = 1
        window.close()

def show_param_motion():
    sg.theme('Light Blue 3') 
    layout = [[sg.Text('Введите параметры модели')],
        [sg.Text('Начальное расстояние до акулы: '), sg.Input()],
         [sg.Text('Угол до акулы: '), sg.Input()],
        [sg.Button('Ввести', key='read')] ]
    window = sg.Window('Подводная охота', layout)

    while True:
        event, values = window.read()
        if  event == 'read':
            model = Model(float(values[0]), float(values[1]), True)
            show_graph_motion(model)
        if event == sg.WIN_CLOSED:
            break

    window.close()
    
    
def show_graph_motion(model):  
    if (model.idx == 0):
        sg.popup("Неудача", "Невозможно попасть в акулу, измените параметры")
    else:
        layout = [[sg.Text('Подводному охотнику нужно стрелять', justification='center', font='Helvetica 14')],
                [sg.Text(f'на {model.b_res:.{2}f} градусов или {model.h_res:.{2}f} метров выше акулы', justification='center', font='Helvetica 14')],
                [sg.Canvas(size=(640, 480), key='-CANVAS-')],
                [sg.Button('Отдельные траектории', key='separate'), sg.Button('Таблицы с данными', key='table')] ]
        window = sg.Window('Подводная охота', layout, finalize=True)
        canvas_elem = window['-CANVAS-']
        canvas = canvas_elem.TKCanvas
        fig, ax = plt.subplots()
        ax.grid(True)
        fig_agg = draw_figure(canvas, fig) 
        
        idx = 1
        while True:
            event, values = window.read(timeout=5)
            if event == sg.WIN_CLOSED:
                break
            if event == 'separate':
                window.close()
                show_separate(model)
            if event == 'table':
                window.close()
                show_tables(model)
                
                
            ax.cla()
            ax.grid(True)
            ax.scatter(model.Shark.R+1, model.Shark.H+1, s=1, alpha=0.01)
            if (idx <= model.idx):
                ax.plot(model.Harpoon.X[:idx], model.Harpoon.Y[:idx], c='g', linestyle='-')
                ax.plot(model.Shark.X[:idx],model.Shark.Y[:idx], c='b',linestyle='-')
                ax.scatter(model.Shark.X[idx], model.Shark.Y[idx], s=3000, c='b', marker=shark)
            else:
                ax.plot(model.Harpoon.X[:idx], model.Harpoon.Y[:idx], c='g', linestyle='--')
                ax.plot(model.Shark.X[:model.idx],model.Shark.Y[:model.idx], c='b',linestyle='-')
                ax.scatter(model.Shark.X[model.idx], model.Shark.Y[model.idx], s=3000, c='r', marker=shark)
            fig_agg.draw()
            idx += 1
            if (idx >= len(model.Harpoon.X)):
                idx = 1
        window.close()
        
def show_separate(model):
    layout = [[sg.Text('Траектории движения гарпуна и акулы', justification='left', font='Helvetica 14')],
            [sg.Canvas(size=(640, 480), key='-CANVAS-'), sg.Canvas(size=(640, 480), key='-CANVAS2-')],
            [sg.Button('Общий график', key='graph'), sg.Button('Таблицы с данными', key='table')] ]
    window = sg.Window('Подводная охота', layout, finalize=True)
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    fig, ax = plt.subplots()
    ax.grid(True)
    fig_agg = draw_figure(canvas, fig) 
    ax.grid(True)
    ax.plot(model.Harpoon.X[:model.idx+1], model.Harpoon.Y[:model.idx+1], c='g', linestyle='-')
    ax.plot(model.Harpoon.X[model.idx+1:], model.Harpoon.Y[model.idx+1:], c='g', linestyle='--')
    fig_agg.draw()
    
    canvas_elem = window['-CANVAS2-']
    canvas = canvas_elem.TKCanvas
    fig, ax = plt.subplots()
    ax.grid(True)
    fig_agg = draw_figure(canvas, fig) 
    ax.grid(True)
    ax.plot(model.Shark.X[:model.idx+1],model.Shark.Y[:model.idx+1], c='b',linestyle='-')
    ax.scatter(model.Shark.X[model.idx], model.Shark.Y[model.idx], s=3000, c='r', marker=shark)
    ax.plot(model.Shark.X[model.idx+1:],model.Shark.Y[model.idx+1:], c='b',linestyle='--')
    fig_agg.draw()
    
    while True:
        event, values = window.read(timeout=5)
        if event == sg.WIN_CLOSED:
            break
        if event == 'graph':
            window.close()
            if (model.Shark.V0 != 0):
                show_graph_motion(model)
            else:
                show_graph_no_motion(model)
        if event == 'table':
            window.close()
            show_tables(model)

def show_tables(model):
    model.table()
    
    layout = [[sg.Text('Данные о движении гарпуна и акулы', justification='left', font='Helvetica 14')],
            [sg.Table(values=model.data, headings=model.heading, max_col_width=35,
                    # background_color='light blue',
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=9,
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    row_height=35)],
            [sg.Button('Общий график', key='graph'), sg.Button('Отдельные траектории', key='separate')] ]
    window = sg.Window('Подводная охота', layout, finalize=True)
    
    
    while True:
        event, values = window.read(timeout=5)
        if event == sg.WIN_CLOSED:
            break
        if event == 'graph':
            window.close()
            if (model.Shark.V0 != 0):
                show_graph_motion(model)
            else:
                show_graph_no_motion(model)
        if event == 'separate':
            window.close()
            show_separate(model)
    
def main():
    show_level()
    
if __name__ == "__main__":
    main()