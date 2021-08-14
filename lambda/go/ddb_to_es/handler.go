package main

import (
	"log"
	"context"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
)

/*
Invoked via DynamoDB event stream
*/

var (
	sess = session.Must(session.NewSession(&aws.Config{
		Region:   aws.String("us-east-1"),
		Endpoint: aws.String("http://aws-stack:4566")}))

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