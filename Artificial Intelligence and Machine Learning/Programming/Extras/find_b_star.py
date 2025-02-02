from scipy.optimize import root_scalar
import sys

# Define the function f(b)
def f(b):
    return (N + 1) - (1 - b**(d+1)) / (1 - b)

if __name__ == '__main__':
    N = int(sys.argv[1])
    d = int(sys.argv[2])

    if d >= N:
        print(f"To find a solution, the number of nodes must be at least d+1 (in your case {d+1})")
        quit()

    # Solve using root_scalar
    try:
        result = root_scalar(f, bracket=[0.9, N], method='brentq')  # Use Brent's method
    except ZeroDivisionError as e:
        print("Values of 1 don't mix well with the optimisation!")
    else:
        print("scipy.optimize result:", result.root)