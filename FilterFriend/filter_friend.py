import numpy as np
import napari
import sys


if __name__ == '__main__':

    # print help message
    if isinstance(sys.argv[1], str) and sys.argv[1] in ('-h', '--h', '-help', '--help'):
        print("""
             ~*~~**~~~*** FilterFriend ***~~~**~~*~
        help message
        """)
        sys.exit()


    # load datasets
    image = nrrd.read(sys.argv[1])[0].transpose(2,1,0)
    spots = np.loadtxt(sys.argv[2])
    spacing = np.array(sys.argv[3].split('x'))

    # instantiate viewer
    viewer = napari.Viewer()
