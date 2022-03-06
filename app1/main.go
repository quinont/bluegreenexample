package main

import (
    "fmt"
    "net/http"
    "log"
    "os"
)

func hc(w http.ResponseWriter, req *http.Request) {
    fmt.Fprintf(w, "Ok")
}

func status(w http.ResponseWriter, req *http.Request) {
    hostname, err := os.Hostname()
    if err != nil {
		fmt.Println(err)
		hostname = "pedrito"
	}
    log.Printf("Someone is calling status")
    w.Header().Set("Content-Type", "application/json")
    fmt.Fprintf(w, "{\"Server\": \"%s\", \"message\": \"This is the version v1\"}", hostname)
}

func main() {
    log.Print("Starting...")

    http.HandleFunc("/app1/status", status)
    http.HandleFunc("/hc", hc)

    http.ListenAndServe(":80", nil)
}
