package main

import (
	"log"
	"context"
	"github.com/aws/aws-lambda-go/lambda"
)

type Event struct {
	Records []Record `json:"event"`
}

type Record struct {

}

func HandleRequest(ctx context.Context, event Event) (string, error) {
	log.Printf("Handling %d records", len(event.Records))
	return "", nil
}

func main() {
	lambda.Start(HandleRequest)
}