#!/bin/bash
xhost +
docker run -it --runtime nvidia --name fall \
  -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
  -v /opt/nvidia/deepstream/deepstream-5.0/sources/apps/sample_apps/deepstream-fall-detection/configs:/opt/nvidia/deepstream/deepstream-5.0/sources/apps/sample_apps/deepstream-fall-detection/configs \
  fall-detection:nano-1.0.0
