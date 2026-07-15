FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /out/raglens-collector ./cmd/raglens-collector

FROM alpine:3.20

RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /out/raglens-collector /usr/local/bin/raglens-collector

EXPOSE 4319

ENV RAGLENS_COLLECTOR_ADDR=:4319

CMD ["raglens-collector"]
