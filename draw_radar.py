import tkinter as tk
import serial.tools.list_ports
from math import sin, cos, pi

port = list(serial.tools.list_ports.comports())[0].device       # get communication port
connection = serial.Serial(port, 9600, timeout=1)               # connect to serial monitor
canvas_w = 720                                                  # canvas width
canvas_h = 400                                                  # canvas height
radius = 300                                                    # radar radius
max_distance = 200                                              # radar max distance
scale_factor = radius / max_distance                            # used to scale from real life distance to radar units
canvas_bg = '#022801'                                           # canvas background color
radar_bg = '#022801'                                            # radar background color
radar_circles = '#01FF01'                                       # radar circles color
radar_lines = '#02CD01'                                         # radar lines color
radar_beam = '#01FF01'                                          # radar beam color
radar_object = '#017101'                                        # radar found object color
radar_text = '#01FF01'                                          # text above radar color
radar_beam_lines = []                                           # list to save radar beam lines' ids
radar_object_lines = [0] * 181                                  # list to save radar object lines' ids


def _create_circle_arc(self, x, y, r, **kwargs):                # function to create circle arcs in tkinter's canvas
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)


def _create_circle(self, x, y, r, **kwargs):                    # function to create circles in tkinter's canvas
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def loop():                                                     # looping function to draw radar's scans
    if connection.in_waiting:                                   # if there are bits waiting to be read on serial
        line = connection.readline().strip().decode('ascii')    # take one line at a time
        values = line.split(',')                                # and split by ','
        if len(values) == 2:
            angle = int(values[0])                              # save angle value
            distance_real = int(values[1])                      # save distance value (before scaling)
            distance = int(int(values[1]) * scale_factor)       # saved scaled distance value
            radians = (-angle) * pi / 180                       # calculate angle in radians
            # draw radar beam lines
            radar_beam_lines.append(canvas.create_line(canvas_w / 2, canvas_h, canvas_w / 2 + radius * cos(radians),
                                                       canvas_h + radius * sin(radians), fill=radar_beam, width=8))
            canvas.delete(radar_object_lines[angle])            # delete previously drawn line at angle's position
            if 0 < distance <= max_distance:                    # if a correct distance is measured, draw a new line
                radar_object_lines[angle] = (
                    canvas.create_line(canvas_w / 2 + radius * cos(radians), canvas_h + radius * sin(radians),
                                       canvas_w / 2 + distance * cos(radians), canvas_h + distance * sin(radians),
                                       fill=radar_object, width=10, smooth=1))

            if len(radar_beam_lines) == 5:                      # if the beam has 5 lines drawn
                canvas.delete(radar_beam_lines.pop(0))          # delete the oldest one

            canvas.tag_raise(circle_300)                        # place circles arcs, lines and texts above all drawings
            canvas.tag_raise(circle_300_text)
            canvas.tag_raise(circle_200)
            canvas.tag_raise(circle_200_text)
            canvas.tag_raise(circle_100)
            canvas.tag_raise(circle_100_text)
            canvas.tag_raise(circle_50)
            canvas.tag_raise(circle_50_text)
            canvas.tag_raise(deg_0_line)
            canvas.tag_raise(deg_0_text)
            canvas.tag_raise(deg_45_line)
            canvas.tag_raise(deg_45_text)
            canvas.tag_raise(deg_90_line)
            canvas.tag_raise(deg_90_text)
            canvas.tag_raise(deg_135_line)
            canvas.tag_raise(deg_135_text)
            canvas.tag_raise(deg_180_line)
            canvas.tag_raise(deg_180_text)
            for line in radar_beam_lines:
                canvas.tag_raise(line)

            angle_sv.set(str(angle))                            # save angle's value as a tkinter StringVar variable
            distance_sv.set(str(distance_real))                 # save distance's value as a tkinter StringVar variable
    root.after(15, loop)                                        # call looping function again after 15ms


tk.Canvas.create_circle = _create_circle                        # attach created drawing functions to tkinter's Canvas
tk.Canvas.create_circle_arc = _create_circle_arc                # class

root = tk.Tk()                                                  # instantiate tkinter Tk class
root.config(background=canvas_bg)                               # set background color
angle_sv = tk.StringVar()                                       # create tkinter StringVar objects
distance_sv = tk.StringVar()

# create canvas for drawing graph
canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, borderwidth=0, highlightthickness=0, bg=canvas_bg)
canvas.grid(row=1)
# create frame for text boxes
frame = tk.Frame(root, width=canvas_w, bg=canvas_bg, pady=10)
frame.grid(row=0)

# create text labels
tk.Label(frame, text='\tAngle: ', fg=radar_text, bg=canvas_bg, justify='left', anchor='w', font=("Courier", 15)).grid(
    row=0, column=0)
tk.Label(frame, textvariable=angle_sv, fg='white', bg=canvas_bg, justify='left', anchor='e', width=3,
         font=("Courier", 15)).grid(row=0, column=1)
tk.Label(frame, text='\N{DEGREE SIGN}', fg=radar_text, bg=canvas_bg, justify='left', anchor='w',
         font=("Courier", 15)).grid(row=0, column=2)
tk.Label(frame, text='', fg=radar_text, bg=canvas_bg, justify='left', anchor='w', width=25, font=("Courier", 15)).grid(
    row=0, column=3)
tk.Label(frame, text='Distance: ', fg=radar_text, bg=canvas_bg, justify='left', anchor='w', font=("Courier", 15)).grid(
    row=0, column=4)
tk.Label(frame, textvariable=distance_sv, fg='white', bg=canvas_bg, justify='left', anchor='e', width=3,
         font=("Courier", 15)).grid(row=0, column=5)
tk.Label(frame, text='cm\t', fg=radar_text, bg=canvas_bg, justify='left', anchor='w', font=("Courier", 15))\
    .grid(row=0, column=6)

# draw circle arcs and distance markings
circle_300 = canvas.create_circle_arc(canvas_w / 2, canvas_h, 300, outline=radar_circles, width=6, start=0, end=180)
circle_300_text = canvas.create_text(canvas_w / 2 + 20, canvas_h - 300 - 10, text=str(int(300 / scale_factor)) + 'cm',
                                     fill=radar_circles)
circle_200 = canvas.create_circle_arc(canvas_w / 2, canvas_h, 200, outline=radar_circles, width=5, start=0, end=180)
circle_200_text = canvas.create_text(canvas_w / 2 + 20, canvas_h - 200 - 10, text=str(int(200 / scale_factor)) + 'cm',
                                     fill=radar_circles)
circle_100 = canvas.create_circle_arc(canvas_w / 2, canvas_h, 100, outline=radar_circles, width=4, start=0, end=180)
circle_100_text = canvas.create_text(canvas_w / 2 + 20, canvas_h - 100 - 10, text=str(int(100 / scale_factor)) + 'cm',
                                     fill=radar_circles)
circle_50 = canvas.create_circle_arc(canvas_w / 2, canvas_h, 50, outline=radar_circles, width=3, start=0, end=180)
circle_50_text = canvas.create_text(canvas_w / 2 + 20, canvas_h - 50 - 10, text=str(int(50 / scale_factor)) + 'cm',
                                    fill=radar_circles)

# draw background grid
lines = 20
for i in range(0, canvas_w, canvas_w // lines):
    canvas.create_line(i, 0, i, canvas_h, fill='grey')
canvas.create_line(canvas_w - 1, 0, canvas_w - 1, canvas_h, fill='grey')
for i in range(0, canvas_h, canvas_h // lines):
    canvas.create_line(0, i, canvas_w, i, fill='grey')
canvas.create_line(0, canvas_h - 1, canvas_w, canvas_h - 1, fill='grey')

# draw 0 degree line
deg_0_line = canvas.create_line(canvas_w / 2, canvas_h, 97 / 100 * canvas_w, canvas_h - 1, fill=radar_lines)
deg_0_text = canvas.create_text(95 / 100 * canvas_w, 95 / 100 * canvas_h, text='0\N{DEGREE SIGN}', fill=radar_lines,
                                anchor=tk.NW)

# draw 45 degree line
deg_45_line = canvas.create_line(canvas_w / 2, canvas_h, canvas_w / 2 + 1 / 2 * canvas_w * cos(pi / 4),
                                 canvas_h - 1 / 2 * canvas_w * sin(pi / 4), fill=radar_lines)
deg_45_text = canvas.create_text(canvas_w / 2 + 1 / 2 * canvas_w * cos(pi / 4) - 20,
                                 canvas_h - 1 / 2 * canvas_w * sin(pi / 4) + 20, text='45\N{DEGREE SIGN}',
                                 fill=radar_lines, anchor=tk.NW)

# draw 90 degree line
deg_90_line = canvas.create_line(canvas_w / 2, 1 / 10 * canvas_h, canvas_w / 2, canvas_h, fill=radar_lines)
deg_90_text = canvas.create_text(canvas_w / 2 + 5, 13 / 100 * canvas_h, text='90\N{DEGREE SIGN}', fill=radar_lines,
                                 anchor=tk.NW)

# draw 135 degree line
deg_135_line = canvas.create_line(canvas_w / 2, canvas_h, canvas_w / 2 + 1 / 2 * canvas_w * cos(3 * pi / 4),
                                  canvas_h - 1 / 2 * canvas_w * sin(3 * pi / 4), fill=radar_lines)
deg_135_text = canvas.create_text(canvas_w / 2 + 1 / 2 * canvas_w * cos(3 * pi / 4),
                                  canvas_h - 1 / 2 * canvas_w * sin(3 * pi / 4) + 20, text='135\N{DEGREE SIGN}',
                                  fill=radar_lines, anchor=tk.NW)

# draw 180 degree line
deg_180_line = canvas.create_line(canvas_w / 2, canvas_h, 2 / 100 * canvas_w, canvas_h - 1, fill=radar_lines)
deg_180_text = canvas.create_text(3 / 100 * canvas_w, 95 / 100 * canvas_h, text='180\N{DEGREE SIGN}', fill=radar_lines,
                                  anchor=tk.NW)

# add title to window
root.wm_title("Proiect SI - Aplicatie RADAR")

# call looping function after 1000ms
root.after(1000, loop)

# make sure program does not stop until closed by user
root.mainloop()
