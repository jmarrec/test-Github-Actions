FROM alpine

WORKDIR /app

COPY . .

CMD ["/bin/sh", "-c", "echo 'It works!'"]
