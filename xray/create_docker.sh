# create a docker image
# docker build . < Dockerfile -t shenghh2020/fda_xray_2021:1.0
docker build . < Dockerfile_cuda11 -t shenghh2020/xray_2021_cuda11:1.0

# push docker image to the docker hub
# docker push shenghh2020/fda_xray_2021:1.0
docker push shenghh2020/xray_2021_cuda11:1.0

# bsub -Is -G compute-anastasio -q anastasio-interactive -a 'docker(shenghh2020/fda_xray_2021:1.0)' -gpu "num=4" /bin/bash