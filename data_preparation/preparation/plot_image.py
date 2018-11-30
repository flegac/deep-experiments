import matplotlib.pyplot as plt
import numpy as np

# Generate some data...
x, y = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
x, y = x - x.mean(), y - y.mean()
z = x * np.exp(-x ** 2 - y ** 2)

# Plot the grid
plt.imshow(z)
plt.gray()
plt.show()
