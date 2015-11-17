
FROM ubuntu:latest
MAINTAINER FJR Moreews <fjrmoreews@gmail.com>

ENV PATH "$PATH:/usr/bin/registry/"

##&& apt-get update
# Packaged dependencies
RUN mkdir /usr/bin/registry/  && apt-get install -y \
	python2.7 curl libc6 libcurl3 zlib1g
WORKDIR "/usr/bin/registry/"
COPY * /usr/bin/registry/
 
ENTRYPOINT ["/usr/bin/registry/registryClient.sh"]

