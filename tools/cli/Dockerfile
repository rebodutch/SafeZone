FROM python:3.13-slim

COPY tools/cli/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# 安裝 locales 包
RUN apt-get update && apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8

# 設置默認語言環境
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

COPY tools/cli /app
COPY utils /app/utils

ENV PYTHONPATH=/app

RUN echo "alias szio='python /app/io.py'" >> ~/.bashrc

ENTRYPOINT ["bash"]