# FilterFriend
A napari based tool for interactively setting filtering values for EASI-FISH spot detections

# Installation
You should install FilterFriend in a fresh conda environment:
```bash
conda create --name filter_friend python=3.12
conda activate filter_friend
```
Next, clone the FilterFriend repository:
```bash
cd /my/favorite/source/directory
git clone https://github.com/GFleishman/FilterFriend.git
```
Finally, install using setuptools:
```bash
cd FilterFriend
pip install .
```

# Opening FilterFriend
Filter friend is just a python script that runs napari. It has three required arguments:
* Path to a .nrrd image file containing an EASI-FISH probe channel
* Path to a .txt file that contains spot detections from that channel
* The physical voxel spacing of the input image, dimensions separated with 'x', e.g. 0.8x0.5x0.5

So, to open FilterFriend:
```bash
cd /my/favorite/source/directory/FilterFriend
python ./FilterFriend/filter_friend.py /path/to/image/file/c0s3.nrrd /path/to/spots/c0_spots.txt 0.8x0.5x0.5
```

# Using FilterFriend
