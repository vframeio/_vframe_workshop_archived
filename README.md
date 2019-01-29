# VFRAME: Workshop Demos

Dockererized utilities for VFRAME workshops using the command line to extract metadata about images

## Getting Started

*Install Docker*

- Linux, MacOS

*Build Docker*

- build Docker: `./docker_rebuild.sh` (may take a while to download all files)
- start Docker: `./docker_start_osx.sh`
- activate conda environment from: `conda activate vframe_workshop`

### Running Examples

- test the Click app: `python cli_workshop.py`
- run metadata exmample: `python cli_workshop.py metadata`
- see all options: `python cli_workshop.py metadata --help`

### Extract Metadata from an Image

Extract the image width and height to a CSV:

- run: `python cli_workshop.py metadata -i data/input/dog.jpg -o data/output/output.csv`

Extract the image width and height and hash to CSV:

- run: `python cli_workshop.py metadata -i data/input/dog.jpg -o data/output/output.csv --hash`

Extract the image width, height, hash, and EXIF to CSV:

- run: `python cli_workshop.py metadata -i data/input/dog.jpg -o data/output/output.csv --hash --exif`

Extract the image width, height, hash, EXIF, and face count to CSV:

- run: `python cli_workshop.py metadata -i data/input/obama.jpg -o data/output/output.csv --hash --exif --faces`

Extract the image width, height, hash, EXIF, face count, and object count to CSV:

- first, download object detection models: `python cli_workshop.py`
- run: `python cli_workshop.py metadata -i data/input/sheep.jpg -o data/output/output.csv --hash --exif --faces --objects`


### Getting Images/Videos

- To get videos from YouTube use the provided `youtube-dl` utility
- example: `youtube-dl https://www.youtube.com/watch?v=mi4GVqu6I-A`


### Issues

- please only file an issue if there is an issue with the code in this repo
- this is work in progress