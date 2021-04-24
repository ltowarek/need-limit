FROM python:3.9

RUN pip install --upgrade pip

RUN groupadd -g 1000 app
RUN useradd -u 1000 -g app -s /bin/sh -m app
USER app

ENV PATH="/home/app/.local/bin/:${PATH}"
ENV PYTHONPATH="/home/app/.local/lib/python3.8/site-packages:${PYTHONPATH}"

CMD ["/bin/bash"]
