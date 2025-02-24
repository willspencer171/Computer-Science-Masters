"""So, it's a bit hacky, but here's two implementations to get
the weights for linear regression

In doing this, we can also perform the linear regression by generating
predicted response values"""
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# To solve the form
# beta = (X^T X)^-1 (X^T y)
# where X is a matrix with a column of ones, with a column
# of values for x and y is the vector of observed values

x = np.random.standard_exponential((100, 2))
y = np.random.standard_exponential(100)

def solve_least_squares(x: np.ndarray, y: np.ndarray, 
                        optimised=False) -> tuple[np.ndarray, np.ndarray]:
    """Calculates the coefficients of variables in the linear
    regression model
    
    Parameters
    ---
        x : ndarray
            containing values of independent variables
        y : ndarray
            containing values of dependent variables
        optimised : bool
            if True, uses np.linalg.solve() to compute coefficients

    Returns
    ---
        beta : ndarray
            coefficients of regression features
        y_preds : ndarray
            predicted response variable values
    """

    X = np.column_stack((np.ones(x.shape[0]), x))

    XtX = X.T @ X   # @ is matrix multiplication!
    Xty = X.T @ y

    # Compute matrix inversion
    if optimised:
        beta = np.linalg.solve(XtX, Xty)
    else:
        beta = np.linalg.inv(XtX) @ Xty

    # Predicted response is a matrix multiplication
    # of dependents with coefficients. Naturally
    y_pred = X @ beta

    return (beta, y_pred)

def show_3d_regplot(x: np.ndarray[float], y:np.ndarray[float]):
    beta, _ = solve_least_squares(x, y, True)
    fig = plt.figure()
    plot = fig.add_subplot(111, projection='3d')

    plot.scatter(x.T[0], x.T[1], y)

    # Surface plot of predictions
    X1_grid, X2_grid = np.meshgrid(np.linspace(min(x.T[0]), max(x.T[0]), 10),
                                np.linspace(min(x.T[1]), max(x.T[1]), 10))
    Y_pred_grid = beta[0] + beta[1] * X1_grid + beta[2] * X2_grid

    plot.plot_surface(X1_grid, X2_grid, Y_pred_grid, color='red', alpha=0.5)

beta, y_pred = solve_least_squares(x, y, optimised=True)

print(f"Coefficients:\n{beta}")
print(f"Predicted Response:\n{y_pred}")
