FROM python:3.8

ARG ML_FILE=ml-latest-small.zip
ARG ML_URL=https://files.grouplens.org/datasets/movielens/${ML_FILE}

RUN pip install \
        pandas \
        psycopg2 \
        sqlalchemy

WORKDIR /tmp

RUN curl ${ML_URL} -O && \
    unzip ${ML_FILE} && \
	rm -f ${ML_FILE}

ADD app.py /tmp

CMD python app.py