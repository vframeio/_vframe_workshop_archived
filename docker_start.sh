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
                                                 
                                            
Visual Forensics and Advanced Metadata Extraction
"
# Start the docker container with access to USB devices
# Make ports accessible to Jupyter
	#--user docker \
CUR_FILE=$(readlink -f "$0")
CUR_DIR="$(dirname "$CUR_FILE")"
echo $CUR_DIR

docker run -it --rm --privileged \
  --hostname VFRAME-$(hostname|sed -e 's/ubuntu-//') \
	-e DISPLAY=$DISPLAY \
	--volume /tmp/.X11-unix:/tmp/.X11-unix \
	--volume "data_store_workshop:/data_store" \
	--volume "$CUR_DIR:/vframe_workshop" \
	-e DISPLAY=unix$DISPLAY \
  -p $docker_port \
	-e "USER_HTTP=1" $image "$@"
[ "$sshx" = "true" ] && kill %1 # kill backgrounded socat