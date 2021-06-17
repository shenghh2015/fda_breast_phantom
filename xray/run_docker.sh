#docker run -v /home/sh38/docker/data_codes:/data_codes -w /data_codes -i -t test-shenghua:test bash
docker run -v /home/sh38/docker/data_codes:/data_codes -w /data_codes -i -t test-shenghua:test /usr/bin/python data_codes/hello_world.py
