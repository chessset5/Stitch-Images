#!/usr/bin/env python3.12

# https://docs.opencv.org/4.x/d8/d19/tutorial_stitcher.html

"""
Stitching sample
================

Show how to use Stitcher API from python in a simple way to stitch panoramas
or scans.
"""

# Python 2/3 compatibility
from __future__ import print_function

import argparse
import sys
from typing import cast

import cv2 as cv
from cv2 import Mat
from cv2.typing import NumPyArrayNumeric

modes: tuple[int, int] = (cv.Stitcher_PANORAMA, cv.Stitcher_SCANS)

parser = argparse.ArgumentParser(prog="stitching.py", description="Stitching sample.")
parser.add_argument(
    "--mode",
    type=int,
    choices=modes,
    default=cv.Stitcher_PANORAMA,
    help="Determines configuration of stitcher. The default is `PANORAMA` (%d), "
    "mode suitable for creating photo panoramas. Option `SCANS` (%d) is suitable "
    "for stitching materials under affine transformation, such as scans." % modes,
)
parser.add_argument("--output", default="result.jpg", help="Resulting image. The default is `result.jpg`.")
parser.add_argument("img", nargs="+", help="input images")

__doc__ += "\n" + parser.format_help()  # type: ignore


def main() -> None:
    args: argparse.Namespace = parser.parse_args()

    # read input images
    imgs: list[Mat | NumPyArrayNumeric | None] = []
    for img_name in args.img:
        img: Mat | NumPyArrayNumeric | None = cv.imread(cv.samples.findFile(img_name))
        if img is None:
            print("can't read image " + img_name)
            sys.exit(-1)
        imgs.append(img)

    #![stitching]
    stitcher: cv.Stitcher = cv.Stitcher.create(args.mode)
    status, pano = stitcher.stitch(imgs)  # type:ignore

    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % cast(int, status))
        sys.exit(-1)
    #![stitching]

    cv.imwrite(args.output, cast(Mat, pano))
    print("stitching completed successfully. %s saved!" % args.output)

    print("Done")


if __name__ == "__main__":
    print(__doc__)
    main()
    cv.destroyAllWindows()
