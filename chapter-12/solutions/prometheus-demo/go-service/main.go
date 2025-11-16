package main

import (
  "fmt"
  "net/http"
  "github.com/prometheus/client_golang/prometheus"
  "github.com/prometheus/client_golang/prometheus/promhttp"
)

var reqCounter = prometheus.NewCounter(
  prometheus.CounterOpts{
    Name: "go_requests_total",
    Help: "Total number of requests",
  },
)

func main() {
  prometheus.MustRegister(reqCounter)
  http.HandleFunc("/", func(w http.ResponseWriter,
    r *http.Request) {
    reqCounter.Inc()
    fmt.Fprintf(w, "Hello from Go service!")
  })
  http.Handle("/metrics", promhttp.Handler())
  http.ListenAndServe(":8081", nil)
}
