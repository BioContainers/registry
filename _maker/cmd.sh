CMD=$1

source config

docker run --rm -v "$CFG:/src" --name ${NAME}_run grahamc/jekyll rake $CMD
