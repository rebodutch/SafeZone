# Build 
FROM golang:1.24-bookworm AS build
WORKDIR /module
COPY go.mod go.sum /module/
RUN go mod download
COPY app /module/app
RUN go build -o worker ./app/main.go

# Deploy 
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=build /module/worker .
CMD ["./worker"]