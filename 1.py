import numpy as np
import matplotlib.pyplot as plt
import ruptures as rpt
from scipy.interpolate import splrep, splev, UnivariateSpline
# Example data (replace this with your data)
np.random.seed(0)
x = [80,120,150,170,190, 210,230,250, 270, 300, 340, 380]
y = [-2.43, -2.49, -2.52, -2.57, -2.64, -2.7,-2.82,-2.95,-3.0, -3.05,-3.09,-3.14]

new_T = np.linspace(x[0], x[-1], int((x[-1] - x[0])/5) + 1)
new_vth =  UnivariateSpline(x, y,s = 0)
print(len(new_T))
# # Fit a polynomial of degree 2
# coefficients = np.polyfit(x, y, 6)
# polynomial = np.poly1d(coefficients)

# # Generate x values for plotting the polynomial curve
# x_fit = np.linspace(min(x), max(x), 100)
# y_fit = polynomial(x_fit)

# Plotting
plt.scatter(x, y, color='b', s = 20, label='Original Data')
plt.scatter(new_T, new_vth(new_T), color='red', s =5, label='Fitted Polynomial Curve')
print(new_T[14], new_vth(new_T)[14])
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Polynomial Fit')
plt.legend()
plt.show()
