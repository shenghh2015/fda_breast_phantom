docker build . < Dockerfile
docker images

IMAGEID=

docker tag $IMAGEID test-shenghua:test
chcon -Rt svirt_sandbox_file_t /home/sh38/docker/data_codes
docker run -v /home/sh38/docker/data_codes:/data_codes -w /data_codes -i -t test-shenghua:test bash

