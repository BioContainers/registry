source setup

docker stop $NAME || true
docker rm $NAME   || true

docker run -d   -v "$CFG:/src" -p $HOST:$PORT:4000 --name $NAME grahamc/jekyll serve -H 0.0.0.0
