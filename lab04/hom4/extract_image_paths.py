from pathlib import Path

import polars as pl

DATA_DIR = Path(__file__).parent / "data" / "images"
METADATA_PATH = DATA_DIR / "metadata" / "images.csv.gz"
IMAGES_DIR = DATA_DIR / "small"
MIN_SIZE = 1000


def get_image_paths(min_size: int = MIN_SIZE) -> list[str]:
    paths = (
        pl.read_csv(METADATA_PATH)
        .filter((pl.col("width") >= min_size) & (pl.col("height") >= min_size))
        .select((str(IMAGES_DIR) + "/" + pl.col("path")).alias("path"))
        .to_series()
        .to_list()
    )
    return [path for path in paths if Path(path).is_file()]


if __name__ == "__main__":
    image_paths = get_image_paths()
    print(f"Found {len(image_paths)} images with width and height >= {MIN_SIZE}")
    print(*image_paths[:5], sep="\n")
