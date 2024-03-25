FROM golang:1.21.8 AS golang-builder

WORKDIR /go

COPY trade/calculateLevels.go .

RUN go build calculateLevels.go

FROM python:3.12.2 AS python-builder

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

COPY --from=golang-builder /go /bot/trade
