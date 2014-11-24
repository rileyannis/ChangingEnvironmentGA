import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from fitness_function import *

def main():
    ff = Fitness_Function(sphere_function, 0, 2)
    ff.create_fitness2(1)
    ff.set_flipped(True)
    #print fitness2([1,1])
    #plotFitnessFunction(ff.fitness1)
    plotFitnessFunction(ff.fitness2)
    print ff.correlation()

def plotFitnessFunction(function):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    interval = float(512+512)/MOD_SAMPLES
    X = np.arange(-512, 511, interval)
    Y = np.arange(-512, 511, interval)
    X, Y = np.meshgrid(X, Y)
    Z = function([X,Y])
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
    plt.show()

if __name__ == "__main__":
    main()

