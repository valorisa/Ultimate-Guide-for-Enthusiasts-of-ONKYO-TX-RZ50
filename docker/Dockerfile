FROM python:3.11-slim
LABEL maintainer="valorisa" description="Onkyo TX-RZ50 Automation Toolkit"

RUN useradd -m -u 1000 onkyo && \
    mkdir -p /app/scripts /app/logs /app/config && \
    chown -R onkyo:onkyo /app

WORKDIR /app
USER onkyo

COPY scripts/requirements.txt /app/scripts/requirements.txt
RUN pip install --user --no-cache-dir -r /app/scripts/requirements.txt

COPY scripts/ /app/scripts/
COPY config/ /app/config/

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python /app/scripts/health_check.py || exit 1

ENTRYPOINT ["python", "/app/scripts/rs232_control.py"]
CMD ["--help"]
