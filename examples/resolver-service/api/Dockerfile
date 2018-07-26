FROM alpine:3.7
RUN apk --no-cache add python3
COPY apiserver.py /apiserver.py
ENV PYTHONUNBUFFERED 1
CMD ["python3", "apiserver.py"]
