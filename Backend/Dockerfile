FROM hub.ecaps.top/library/python:3.11-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    TZ=Asia/Shanghai

FROM base AS dependencies

COPY requirements.txt .

RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --no-cache-dir -r requirements.txt

FROM base AS final

COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

RUN adduser --disabled-password --gecos "" appuser

COPY . .

RUN if [ ! -f .env ]; then cp -n .env.example .env 2>/dev/null || echo "No .env.example found"; fi

# 设置文件所有者
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:8080"]