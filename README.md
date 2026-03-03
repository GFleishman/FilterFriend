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
Running the command above will launch napari; the first time is a little slow, but it will be faster on subsequent runs.
Napari opens with two layers: the image and the spots, with the spots layer hidden by default. The first thing
you should do is click on the image layer (hcr-image) and play with the contrast limits while scrolling through the
z-stack. The goal is to get an understanding of what content is in the image, as your filtering choices will be
based on how well you match the patterns you see in the image. Be careful and take your time, because some
of the image content can only be seen at different ranges of contrast.

Once you have a good understanding of the image content, you want to turn on the points layer (original-spots).
Scroll through the stack again to get a sense for the types of spots that were found.

Now, you are ready to add a filter. Probably the first filter you want to add is a Percentile Filter, which is
the default, so just click "Add Filter." The percentile filter removes all points whose intensities are below 
a given percentile threshold. Choose a percentile value based on the approximate number of
over-detections you see. This isn't super precise, and you'll be able to run many tests, so just go with
something between 20 and 60. Click "Run Filters."

You'll see that a new layer has been added: filtered-spots. You may want to toggle the original-spots layer
on and off to better see filtered-spots. Scroll through the stack and consider how well the filtered set
matches the pattern(s) you see in the data.

If the channel you are working with has bright densities and you want to exclude spots outside those
densities, then you can add a density filter. Change the Filter Type to Density and click Add Filter.
The density filter works by drawing a sphere around every spot and counting the number of spots
within that sphere. If the number of spots is too low, then the spot is discarded. A reasonable
first value for radius is say 8.0 (that's in microns) and a reasonable neighbor count is 20. Click
Run Filters again. Density filters are a bit slower so you may need to wait a few seconds for it to
finish. If there are still too many spots outside the bright dense areas, then you can decrease
the radius and increase the neighbor count - that will remove more spots overall.

When it's done, the filtered-spots layer will have been updated with the new filtering results. Importantly,
whenever you click "Run Filters," it is starting from the original spots set. That is, multiple clicks on
Run Filters do not stack. This ensures that the result you see is always the direct result of exactly the
set of filters you see on screen.

You can add more filters and experiment to try and match the pattern in the image data. Let's say you're
relatively happy with the filtered-spots but there are a few spots you'd still like to get rid of. You can
always remove spots manually - this is a fully functional napari points layer. Select the filtered-spots layer
(so it's highlighted in blue) and at the top left make sure the arrow is selected (the tooltip says "Select Points").
Then you can select the points you want to remove (draw a box around them) and just hit delete.

When you have settled on a final filtered-spots set, the first thing you should do is screenshot the viewer. This
will record the set of filters you used to obtain the final spot set. Next, you can click File --> Save Selected Layers
to save the filtered-spots set (make sure filtered-spots is actually the currently selecte layer of course).
