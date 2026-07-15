FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /out/sledtrace-collector ./cmd/sledtrace-collector

FROM alpine:3.20

RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /out/sledtrace-collector /usr/local/bin/sledtrace-collector

EXPOSE 4319

ENV SLEDTRACE_COLLECTOR_ADDR=:4319

CMD ["sledtrace-collector"]
