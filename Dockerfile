FROM python:3.10-slim

# Recieve build arguments
ARG PIPENV_EXTRA_ARGS

# Change working directory
WORKDIR /app/

# Copy project files
COPY ./ ./

# Install deps
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile $PIPENV_EXTRA_ARGS

CMD sleep 5 \
    && python src/manage.py migrate \
    && python src/manage.py runserver 0.0.0.0:80