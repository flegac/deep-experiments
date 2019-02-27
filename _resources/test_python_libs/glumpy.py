import glumpy
import numpy as np

# Generate some data...
x, y = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
x, y = x - x.mean(), y - y.mean()
z = x * np.exp(-x ** 2 - y ** 2)

window = glumpy.Window(512, 512)
im = glumpy.Image(z.astype(np.float32), cmap=glumpy.colormap.Grey)


@window.event
def on_draw():
    im.blit(0, 0, window.width, window.height)


window.mainloop()
