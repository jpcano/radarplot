# -*- coding: utf-8 -*-

"""
Module that contains the types of the dataset
"""

import pylab as plt
import matplotlib.animation as animation
import numpy as np
                
class Plot (object):
    """Abstract class for common plot actions."""
    def __init__(self, ID, label):
        self.ID = ID
        self.label = label

    def getTitle(self):
        """Return the title of the plot."""
        return  "ID: {}, Label: {} inches".format(self.ID, self.label)

    def getColorbarLabel(self):
        """Returns the label for the colorbar."""
        return 'Reflectivity dBZ'

    def draw(self, filename):
        """If filename is empty, show the plot on the screen.
        Otherwise, save the plot in a file."""
        if (filename):
            plt.savefig(filename)
        else:
            plt.show()
        plt.close()

class Radar (Plot):
    """Abstract class to store all the maps in a target zone plus
    metainformation related to the target."""

    def __init__(self, ID, label):
        self.ID = ID
        self.label = label
        self.stacks = []
        Plot.__init__(self, ID, label)

    class CircularInt (object):
        """"Workaround to generate a circular list of ints."""

        def __init__(self, n):
            self.n = n
            self.i = -1
        
        def next(self):
            """Return the next integer in the circular list."""
            if (self.i == self.n - 1):
                self.i = -1
            self.i += 1
            return self.i

    def addStack(self, stack):
        """Add a stack to the Radar object."""
        self.stacks.append(stack)

    def getStack(self, n):
        """Returns a stack by its position n."""
        return self.stacks[n]

    def getAllStacks(self):
        """Returna list with all the stacks."""
        return self.stacks

    def getSize(self):
        """Returns the number of stacks in the Radar object."""
        return len(self.stacks)
    
    def getID(self):
        """Return a string with the id of the Radar object."""
        return self.ID

    def getLabel(self):
        """Returns a float with the label associated to the Radar."""
        return self.label

    def plot(self, filename='', fps=4):
        """If filename is empty, show the animated plot on the screen.
        Otherwise, save the plot in a mp4 file."""
        fig = plt.figure()
        stackn = self.CircularInt(self.getSize())
        im = self.getStack(stackn.next()).putPlot()
        def updatefig(*args):
            layers = self.getStack(stackn.next()).getAllLayers()
            for i, l in enumerate(layers): 
                layerdata = l.getData()
                im[i].set_array(layerdata)
            return im
        ani = animation.FuncAnimation(fig, updatefig, interval=int(1000/fps), blit=True)
        plt.suptitle(self.getTitle())
        if (filename):
            ani.save(filename, fps=fps, extra_args=['-vcodec', 'libx264'])
            plt.close()
        else:
            self.draw(filename)
            
    def plotThumbnail(self, filename=''):
        """If filename is empty, show a thumbnail of the Radar object on the screen.
        Otherwise, save it in a file."""
        self.getStack(7).putThumbnail()
        self.draw(filename)

    def getAllLayerFeatures(self):
        features = []
        nlayers = self.getStack(0).getSize()
        for l in range(0, nlayers):
            for s in self.getAllStacks():
                features.append(s.getLayer(l).getDataFlatten())
        features = np.array(features)
        return features.reshape(1, -1)[0]

    
class RadarStack (Plot):
    """Abstract class to store the layers of a stack."""

    def __init__(self, radar, stackn):
        self.radar = radar
        self.stackn = stackn
        self.layers = []
        Plot.__init__(self, radar.getID(), radar.getLabel())

    def getSize(self):
        """Returns the number of layers in the Stack."""
        return len(self.layers)

    def addLayer(self, layer):
        """Add a layer to the Stack."""
        self.layers.append(layer)
        
    def getLayer(self, n):
        """Returns a layer identified by its number in the stack."""
        return self.layers[n]

    def getAllLayers(self):
        """Returns a list with all the layers in the Stack."""
        return self.layers

    def putPlot(self):
        """Draw (buffered) the contents of a Stack plot and returns a list of
        AxesImage."""
        p = []
        fig = plt.figure(1)
        for i in range(0, self.getSize()):
            plt.subplot(self.getSize() / 2, 2, i + 1)
            im = self.getLayer(i).putPlot()
            p.append(im)
            plt.ylabel('Height ' + str(i))

        # place the colorbar in its own axis
        plt.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.11, 0.02, 0.77])
        cbar = fig.colorbar(p[0], cax=cbar_ax)
        cbar.set_label(self.getColorbarLabel())
        return p

    def putThumbnail(self):
        """Draw (buffered) a thumnail of the Stack without borders and axes."""
        fig = plt.figure(1, figsize=(2.5,2.5))
        for i in range(0, self.getSize()):
            plt.subplot(self.getSize() / 2, 2, i + 1)
            self.getLayer(i).putPlot()
            plt.axis('off')
        plt.subplots_adjust(wspace=0.05, hspace=0.05,left=0.01,
                            right=0.99, top=0.99, bottom=0.01)
        
    def plot(self, filename=''):
        """Plot the Stack on a file or on the screen."""
        plt.suptitle(self.getTitle())
        self.putPlot()
        self.draw(filename)
    
class RadarLayer (Plot):
    """Abstract class to stores the dBZ values of the map grid."""

    def __init__(self, data, radar, stackn, layern):
        self.data = data
        self.radar = radar
        self.stackn = stackn
        self.layern = layern
        self.dim = len(self.data)
        Plot.__init__(self, radar.getID(), radar.getLabel())

    def getSize(self):
        """Returns the number rows in the layer."""
        return self.dim

    def getData(self):
        """Returns a coy of the 2d array that represents the layer."""
        return self.data[:]

    def getDataFlatten(self):
        return self.getData().reshape(1, -1)[0]
    
    def getValue(self, x, y):
        """Get a specific value at (x, y) in the layer."""
        return self.data[x][y]

    def putPlot(self):
        """Draw (buffered) the layer."""
        return plt.imshow(self.data, cmap='jet',
                          interpolation='gaussian', vmin=0, vmax=190)

    def plot(self, filename=''):
        """Plot the layer, saving it in a file or displaying it on the screen."""
        plt.suptitle(self.getTitle())
        self.putPlot()
        plt.colorbar().set_label(self.getColorbarLabel())
        self.draw(filename)
