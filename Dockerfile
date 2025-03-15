FROM ubuntu:latest
LABEL authors="denis"

ENTRYPOINT ["top", "-b"]