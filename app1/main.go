package main

import (
    "fmt"
    "net/http"
    "log"
    "os"
    "math/rand"
    "time"
    "strconv"
)

func hc(w http.ResponseWriter, req *http.Request) {
    fmt.Fprintf(w, "Ok")
}

func getEnv(key, fallback string) string {
    value, exists := os.LookupEnv(key)
    if !exists {
        value = fallback
    }
    return value
}

func status(w http.ResponseWriter, req *http.Request) {
    hostname, err := os.Hostname()
    if err != nil {
		fmt.Println(err)
		hostname = "pedrito"
	}
    w.Header().Set("Content-Type", "application/json")

    rand.Seed(time.Now().UnixNano())
    errorThresholdStr := getEnv("ERRORTHRESHOLD", "95")
    errorThresholdInt, err := strconv.Atoi(errorThresholdStr)
    if err != nil {
        errorThresholdInt = 95
    }

    if (rand.Intn(100) < errorThresholdInt ) {
        log.Printf("Oh nooo, we have an Error here!!, help!!!!")
        w.WriteHeader(500)
        fmt.Fprintf(w, "{\"Server\": \"%s\", \"message\": \"WE HABE A ERRO!! (v4)\"}", hostname)
        return
    }

    log.Printf("Someone is calling status")
    fmt.Fprintf(w, "{\"Server\": \"%s\", \"message\": \"This is the version v4\"}", hostname)
}

func main() {
    log.Print("Starting...")

    http.HandleFunc("/app1/status", status)
    http.HandleFunc("/hc", hc)

    http.ListenAndServe(":80", nil)
}
