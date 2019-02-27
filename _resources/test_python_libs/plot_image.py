import matplotlib.pyplot as plt
import numpy as np

# Generate some data...
x, y = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
x, y = x - x.mean(), y - y.mean()
z = x * np.exp(-x ** 2 - y ** 2)

zz = np.array(z)
print(zz.shape)

# Plot the grid
plt.imshow(z)
plt.gray()
plt.show()

img = np.random.rand(256, 256, 3)

plt.imshow(img)
plt.colormaps()
plt.show()
