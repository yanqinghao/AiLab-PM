NAMESPACE=("shuzhi-amd64")
for i in ${NAMESPACE[*]}
do
    docker build --build-arg NAME_SPACE=${i} -t registry.cn-shanghai.aliyuncs.com/${i}/pm-docker:$1 -f docker/docker_pm/Dockerfile .
    docker build --build-arg NAME_SPACE=${i} -t registry.cn-shanghai.aliyuncs.com/${i}/pm-stream:$1 -f docker/stream_pm/Dockerfile .

    docker push registry.cn-shanghai.aliyuncs.com/${i}/pm-docker:$1
    docker push registry.cn-shanghai.aliyuncs.com/${i}/pm-stream:$1
done