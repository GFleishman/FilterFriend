import setuptools

setuptools.setup(
    name="FilterFriend",
    version="0.0.0",
    author="Greg M. Fleishman",
    author_email="fleishmang@janelia.hhmi.org",
    description="A napari based tool for interactively filtering EASI-FISH spot detections",
    url="https://github.com/gfleishman/FilterFriend",
    license="BSD-3",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'fishspot',
        'pynrrd',
        'napari',
    ]
)

