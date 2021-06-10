FROM python:slim-stretch

RUN mkdir -p /usr/share/man/man1 \
   && apt-get update \
   && apt-get install -y --no-install-recommends \
   openjdk-8-jre \
   graphviz \ 
   wget \
   && cd /tmp \
   && wget https://sourceforge.net/projects/plantuml/files/plantuml.1.2021.5.jar/download \
   && mv download /usr/local/bin/plantuml.jar

RUN pip install --no-cache-dir \
	'Sphinx==3.5.4' \
	'sphinx-autobuild==2021.3.14' \
	'myst-parser==0.13.7' \
	'sphinx_panels==0.5.2' \
	'ablog==0.10.19' \
	'sphinxcontrib-plantuml==0.21' \
	'sphinx-markdown-tables==0.0.15' \
	'sphinxcontrib-openapi==0.7.0' \
	'pydata_sphinx_theme==0.6.3' \
	'sphinxcontrib.gist==0.1.0'

RUN mkdir -p /usr/src/plantuml

WORKDIR /usr/src/app
COPY ./source /usr/src/app/source