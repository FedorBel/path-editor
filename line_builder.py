from matplotlib import pyplot as plt
from dataclasses import dataclass
from scipy import interpolate
import numpy as np


class LineBuilder:
    @dataclass
    class PressData:
        idx: int = 0
        x_value: float = 0
        y_value: float = 0
        new_x_value: float = 0
        new_y_value: float = 0

    def __init__(self):
        self.isInit = False
        self.pickEvent = False
        self.cidpress = fig.canvas.mpl_connect("button_press_event", self.on_press)
        # self.press = None
        self.press = self.PressData()
        self.spline = None

    def connect(self):
        "connect to all the events we need"
        self.cidpress = fig.canvas.callbacks.connect("pick_event", self.on_pick)
        self.cidrelease = fig.canvas.callbacks.connect(
            "button_release_event", self.on_release
        )
        self.cidmotion = fig.canvas.callbacks.connect(
            "motion_notify_event", self.on_motion
        )

    def update_spline(self):
        if len(self.xs) < 9:
            return

        # Fit
        points = list(zip(self.xs, self.ys))
        sorted_points = sorted(list(zip(self.xs, self.ys)), key=lambda k: k[0])

        sorted_x = [i[0] for i in sorted_points]
        sorted_y = [i[1] for i in sorted_points]

        N = 100
        n_interior_knots = 5
        qs = np.linspace(0, 1, n_interior_knots + 2)[1:-1]
        knots = np.quantile(sorted_x, qs)
        x_new = np.linspace(min(self.xs), max(self.xs), N)
        # y_new = np.linspace(min(self.ys), max(self.ys), N)
        tck = interpolate.splrep(sorted_x, sorted_y, t=knots, k=3)
        y_fit = interpolate.BSpline(*tck)(x_new)

        # tck = interpolate.splrep(self.xs, self.ys, s=0, k=3)
        # x_new = np.linspace(min(self.xs), max(self.xs), 100)
        # y_fit = interpolate.BSpline(*tck)(x_new)
        if self.spline == None:
            (spline,) = ax.plot(x_new, y_fit)
            self.spline = spline
        else:
            self.spline.set_data(x_new, y_fit)
        self.spline.figure.canvas.draw()

    def on_press(self, event):
        # print("click", event)
        if not self.isInit and event.inaxes:
            print("NOT INIT")
            self.isInit = True
            global ax
            (line,) = ax.plot(
                [event.xdata], [event.ydata], "ro", markersize=14, picker=5
            )
            self.line = line
            self.xs = list(line.get_xdata())
            self.ys = list(line.get_ydata())
            self.line.figure.canvas.draw()
            self.connect()
            # self.cidpick = fig.canvas.callbacks.connect("pick_event", self.on_pick)
            return

        if event.inaxes != self.line.axes:
            print("NOT IN AXES")
            return

        if self.pickEvent:
            self.pickEvent = False
            return

        print("APPEND")
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        self.update_spline()

    def on_pick(self, event):
        self.pickEvent = True
        artist = event.artist
        xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
        x, y = artist.get_xdata(), artist.get_ydata()
        ind = event.ind
        self.press = ind[0], x[ind[0]], y[ind[0]], xmouse, ymouse
        self.update_spline()
        # print("Artist picked:", event.artist)
        # print("{} vertices picked".format(len(ind)))
        # print("Pick between vertices {} and {}".format(min(ind), max(ind) + 1))
        # print("x, y of mouse: {:.2f},{:.2f}".format(xmouse, ymouse))
        # print("Data point:", x[ind[0]], y[ind[0]])
        # print()

    def on_motion(self, event):
        "on motion we will move the rect if the mouse is over us"
        if self.press is None:
            return
        if event.inaxes != self.line.axes:
            return
        idx, x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        # print 'x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f'%(x0, xpress, event.xdata, dx, x0+dx)
        # self.rect.set_x(x0 + dx)
        # self.rect.set_y(y0 + dy)
        self.xs[idx] = x0 + dx
        self.ys[idx] = y0 + dy
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        # self.update_spline()

    def on_release(self, event):
        "on release we reset the press data"
        self.press = None
        self.line.figure.canvas.draw()
        # self.update_spline()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("click to build line segments")
plt.autoscale(False)
linebuilder = LineBuilder()

plt.show()
