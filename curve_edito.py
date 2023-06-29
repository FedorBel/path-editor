import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

points = []


class PathBuilder:
    def _init_(self):
        self.points


pick_event = False


def onclick(event):
    global pick_event
    print(
        "button=%d, x=%d, y=%d, xdata=%f, ydata=%f"
        % (event.button, event.x, event.y, event.xdata, event.ydata)
    )
    if not pick_event:
        plt.plot(event.xdata, event.ydata, "o", markersize=14, picker=5)
        points.append((event.xdata, event.ydata))
        fig.canvas.draw()

    pick_event = False


def on_move(event):
    if event.inaxes:
        print(
            f"data coords {event.xdata} {event.ydata},",
            f"pixel coords {event.x} {event.y}",
        )


# binding_id = plt.connect("motion_notify_event", on_move)


def on_pick(event):
    global pick_event
    pick_event = True
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    print("Artist picked:", event.artist)
    print("{} vertices picked".format(len(ind)))
    print("Pick between vertices {} and {}".format(min(ind), max(ind) + 1))
    print("x, y of mouse: {:.2f},{:.2f}".format(xmouse, ymouse))
    print("Data point:", x[ind[0]], y[ind[0]])
    print()


cid = fig.canvas.mpl_connect("button_press_event", onclick)
fig.canvas.callbacks.connect("pick_event", on_pick)
plt.show()
