package main

import (
	"bytes"
	"context"
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	elastic "github.com/elastic/go-elasticsearch"
	"log"
	"os"
	"strconv"
)

/* DynamoDB Event Stream Handler */

var (
	// Elasticsearch
	indexName 	string
	es 			*elastic.Client
)

type WikiRecord struct {
	ID			int64	`json:"id"`
	Term		string	`json:"term"`
	Created		string	`json:"date_added"`
	Updated		string	`json:"date_updated"`
}

func HandleRequest(ctx context.Context, event events.DynamoDBEvent) (string, error) {
	log.Printf("Handling [%d] DDB Event Stream Records", len(event.Records))
	for _, e := range event.Records {
		switch e.EventName {
		case "INSERT":
			var payload WikiRecord
			data := e.Change.NewImage
			for k, v := range data {
				switch k {
				case "id":
					id, _ := v.Integer()
					payload.ID = id
				case "term":
					payload.Term = v.String()
				case "date_updated":
					payload.Updated = v.String()
				case "date_added":
					payload.Created = v.String()
				}
			}
			body, _ := json.Marshal(payload)
			_, err := es.Index(
				indexName,
				bytes.NewReader(body), // Document body
				es.Index.WithDocumentID(strconv.Itoa(int(payload.ID))), // Document ID
				es.Index.WithRefresh("true"))
			if err != nil {
				log.Printf("could not insert into elasticsearch: %v", err)
				// todo: SES notification
			}
		//case "MODIFY":
		//	es.Update()
		}
	}
	return "", nil
}

func init() {
	var err error
	// index
	indexName = os.Getenv("ES_INDEX_NAME")
	// init AWS Services
	//awsCfg := &aws.Config{
	//	Endpoint: aws.String("AWS_LOCAL_ENDPOINT")}
	//sess = session.Must(session.NewSession(awsCfg))
	//ddb = dynamodb.New(sess)
	// init ES
	esCfg := elastic.Config{
		Addresses: []string{os.Getenv("ELASTICSEARCH_URL")}}
	es, err = elastic.NewClient(esCfg)
	if err != nil {
		log.Fatalf("could not create es client: %v", err)
	}
	log.Println(es.Info())
}

func main() {
	lambda.Start(HandleRequest)
}
