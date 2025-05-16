FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

RUN yum install -y gcc make curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY . .

# Disable poetry venvs
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-root

CMD ["main.handler"]