FROM nvcr.io/nvidia/deepstream-l4t:5.0-dp-20.04-samples

RUN apt-get update

RUN apt-get install -y libglib2.0-dev libjson-glib-dev uuid-dev gcc g++ && \
  apt-get install -y libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstrtspserver-1.0-dev libx11-dev

ADD . /opt/nvidia/deepstream/deepstream-5.0/sources/apps/sample_apps/deepstream-fall-detection/

WORKDIR /opt/nvidia/deepstream/deepstream-5.0/sources/apps/sample_apps/deepstream-fall-detection

RUN cp nvdsmeta_schema.h /opt/nvidia/deepstream/deepstream-5.0/sources/includes && \
  cp nvmsgconv.cpp /opt/nvidia/deepstream/deepstream-5.0/sources/libs/nvmsgconv && \
  cd /opt/nvidia/deepstream/deepstream-5.0/sources/libs/nvmsgconv/ && make && make install && \
  cd /opt/nvidia/deepstream/deepstream-5.0/sources/gst-plugins/gst-nvmsgbroker && make && make install && \
  cd /opt/nvidia/deepstream/deepstream-5.0/sources/gst-plugins/gst-nvmsgconv && make && make install && \
  ldconfig

RUN cd /opt/nvidia/deepstream/deepstream-5.0/sources/apps/sample_apps/deepstream-fall-detection/ && make clean && make

ENTRYPOINT ["/bin/bash", "configs/main.sh"]