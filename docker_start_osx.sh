#!/bin/bash
# Startup script for docker image

xhost +local:docker

image=vframeio/vframe_workshop
docker images $image


# Jupyter notebook port
while getopts 'p:' flag; do
  case "${flag}" in
    p) port="${OPTARG}";;
    *) error "Unexpected option ${flag}" ;;
  esac
done

if [ ! -z "$port" ]; then
    echo "Port selected: $port"
else
    port="9090"
fi
docker_port="$port:$port"


echo "
 __      ________ _____            __  __ ______ 
 \ \    / /  ____|  __ \     /\   |  \/  |  ____|
  \ \  / /| |__  | |__) |   /  \  | \  / | |__   
   \ \/ / |  __| |  _  /   / /\ \ | |\/| |  __|  
    \  /  | |    | | \ \  / ____ \| |  | | |____ 
     \/   |_|    |_|  \_\/_/    \_\_|  |_|______|
                                                 
                                            
Visual Forensics and Metadata Extraction

1) run: 'conda activate vframe_workshop'
2) run 'python cli_workshop.py'
3) download models 'python cli_workshop.py download_models'
4) grab a few images
5) create hash 'python cli_workshop.py metadata -i data/input/sheep.jpg -o data/output/output.csv --hash'
7) check it: 'cat data/output/output.csv'
8) extract exif 'python cli_workshop.py metadata -i data/input/sheep.jpg -o data/output/output.csv --exif'
9) extract faces 'python cli_workshop.py metadata -i data/input/obama.jpg -o data/output/output.csv --faces'
10) find objects 'python cli_workshop.py metadata -i data/input/sheep.jpg -o data/output/output.csv --objects'
11) you can also chain these commands. Try adding --hash --exif --faces --objects
11) check results: 'cat data/output/output.csv'
 "

CUR_DIR=`pwd`

docker run -it --rm --privileged \
  --hostname VFRAME \
	--volume "data_store_workshop:/data_store" \
	--volume "$CUR_DIR:/vframe_workshop" \
	-e "USER_HTTP=1" $image "$@"