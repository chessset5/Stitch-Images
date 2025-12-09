#!/usr/bin/env python3.12

# https://docs.opencv.org/4.x/d8/d19/tutorial_stitcher.html

from pathlib import Path
from typing import Any

from numpy import dtype, floating, integer

DIR: Path = Path(__file__).parent

DATA_DIR: Path = DIR / "data"

import cv2
from cv2 import STITCHER_OK, Mat, Stitcher
from cv2.typing import MatLike, NumPyArrayNumeric

Stitcher_Status = int
STITCHER_SCANS: int = 1


def stitch_mats(mats: list[MatLike]) -> tuple[Stitcher_Status, MatLike]:
    # stitch them together
    stitcher: Stitcher = Stitcher.create(mode=STITCHER_SCANS)
    result: tuple[Stitcher_Status, MatLike] = stitcher.stitch(images=mats)
    return result


def stitch_path(path: Path) -> MatLike:
    # grab images
    images: list[Path] = [f for f in DATA_DIR.iterdir() if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".tif", ".tiff"]]
    image_binaries: list[MatLike] = []
    for img in images:
        image_matrix: Mat | NumPyArrayNumeric | None = cv2.imread(filename=str(img))
        if image_matrix is None:
            continue
        image_binaries.append(image_matrix)

    result: tuple[Stitcher_Status, MatLike] = stitch_mats(image_binaries)

    if result[0] != STITCHER_OK:
        raise Exception(f"Stitching error for {path}")
    return result[1]


def main() -> None:

    top_image: MatLike = stitch_path(DATA_DIR / "top")
    middle_image: MatLike = stitch_path(DATA_DIR / "middle")
    bottom_image: MatLike = stitch_path(DATA_DIR / "bottom")

    result: tuple[Stitcher_Status, MatLike] = stitch_mats(mats=[top_image, middle_image, bottom_image])
    if result[0] != STITCHER_OK:
        raise Exception(f"Stitching error for {DATA_DIR}")

    cv2.imwrite(filename=str(DIR / "stitch.jpg"), img=result[1])


if __name__ == "__main__":
    main()
