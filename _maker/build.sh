source setup

docker run --rm -v "$CFG:/src" --name ${NAME}_build grahamc/jekyll build
