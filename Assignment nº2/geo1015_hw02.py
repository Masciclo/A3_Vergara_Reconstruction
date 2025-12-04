# -- geo1015.2025.hw02
# -- [YOUR NAME]
# -- [YOUR STUDENT NUMBER]

import argparse
import json
import sys

import numpy as np
import rasterio

# import startinpy


def main():
    parser = argparse.ArgumentParser(description="My GEO1015.2025 hw02")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    # -- aspect
    process_parser = subparsers.add_parser(
        "aspect", help="Calculate aspect of input file"
    )
    process_parser.add_argument("inputfile", help="Input file (required)")

    # -- gradient
    process_parser = subparsers.add_parser(
        "gradient", help="Calculate gradient of input file"
    )
    process_parser.add_argument("inputfile", help="Input file (required)")

    # -- hillshade
    process_parser = subparsers.add_parser(
        "hillshade", help="Calculate hillshade of input file"
    )
    process_parser.add_argument("inputfile", help="Input file (required)")

    # -- isocontours
    process_parser = subparsers.add_parser(
        "isocontours", help="Output isocontours of input file"
    )
    process_parser.add_argument("inputfile", help="Input file (required)")
    process_parser.add_argument(
        "range", help="Python range for the contours, eg: (0, 1000, 100)"
    )

    args = parser.parse_args()

    # -- load in memory the input DEM
    try:
        # -- this gives you a Rasterio dataset
        # -- https://rasterio.readthedocs.io/en/latest/quickstart.html
        d = rasterio.open(args.inputfile)
    except Exception as e:
        print(e)
        sys.exit()

    # print(args)
    if args.cmd == "aspect":
        print("Aspect!")
    elif args.cmd == "gradient":
        print("gradient!")
    elif args.cmd == "hillshade":
        print("Hillshade!")
    elif args.cmd == "isocontours":
        # - validate the range
        try:
            tmp = list(map(int, args.range.strip("() ").split(",")))
            myrange = range(tmp[0], tmp[1], tmp[2])
            isocontours(d, myrange)
        except Exception:
            parser.error("range invalid")

    some_code_to_help_with_rasterio(d)


def some_code_to_help_with_rasterio(dataset):
    """
    !!! USE THIS CODE !!!

    Some random operations with rasterio are shown below, they don't have
    much meanings.
    They are useful to learn how to read/write GeoTIFF files.
    Use this code for your own function, copy part of it, it's allowed.
    """
    # -- some random things you can do
    # print("name:", d.name)
    print("crs:", dataset.crs)
    print("size:", dataset.shape)
    bbox = dataset.bounds
    middlept = ((bbox[2] - bbox[0]) / 2 + bbox[0], (bbox[3] - bbox[1]) / 2 + bbox[1])
    print(middlept)
    # -- numpy of input
    n1 = dataset.read(1)
    # -- an empty array with all values=0
    # n2 = np.zeros(dataset.shape, dtype=np.int8) #-- you can define the type to use for each cell
    n2 = np.zeros(dataset.shape)
    for i in range(n1.shape[0]):
        for j in range(n1.shape[1]):
            n2[i][j] = 2 * n1[i][j]
    # -- put middlept value=99
    # -- index of p in the numpy raster
    row, col = dataset.index(middlept[0], middlept[1])
    n2[row, col] = 999
    # -- write this to disk
    output_file = "output.tiff"
    with rasterio.open(
        output_file,
        "w",
        driver="GTiff",
        height=n2.shape[0],
        width=n2.shape[1],
        count=1,
        dtype=n2.dtype,
        crs=dataset.crs,
        transform=dataset.transform,
    ) as dst:
        dst.write(n2, 1)
    print("File written to '%s'" % output_file)


def create_dummy_geojson():
    mygeojson = {}
    mygeojson["type"] = "FeatureCollection"
    mygeojson["features"] = []
    f = {}
    f["type"] = "Feature"
    f["geometry"] = {"type": "LineString", "coordinates": [[0, 0], [10, 10]]}
    f["properties"] = {"height": 100}
    mygeojson["features"].append(f)
    return mygeojson


def isocontours(d, myrange):
    print("Isocontours with range: {}".format(myrange))
    # -- create a dummy GeoJSON file
    mygeojson = create_dummy_geojson()
    # -- write the contours to a GeoJSON file
    with open("iso.geojson", "w") as file:
        file.write(json.dumps(mygeojson, indent=2))
        print("File 'iso.geojson' created.")


if __name__ == "__main__":
    main()
