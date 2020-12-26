package main

import (
	"encoding/json"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/aws/aws-sdk-go/service/sqs"
	"log"
	"os"
	"time"
)

type Consumer struct {
	Ddb              *dynamodb.DynamoDB
	DdbTableName     string
	SqsQUrl          string
	SqsReceiveParams *sqs.ReceiveMessageInput
	Sqs              *sqs.SQS
}

func New() (*Consumer, error) {
	// Need two separate session configs because of localstack env
	sess, err := session.NewSession(&aws.Config{
		Region:   aws.String("us-east-1"),
		Endpoint: aws.String("http://aws-stack:4566"),
	})
	if err != nil {
		return nil, err
	}

	c := Consumer{
		Ddb:          dynamodb.New(sess),
		DdbTableName: os.Getenv("AWS_DDB_TABLE_NAME"),
		Sqs:          sqs.New(sess),
		SqsQUrl:      os.Getenv("AWS_SQS_QUEUE_URL"),
		SqsReceiveParams: &sqs.ReceiveMessageInput{
			QueueUrl:            aws.String(os.Getenv("AWS_SQS_QUEUE_URL")),
			MaxNumberOfMessages: aws.Int64(3),
			VisibilityTimeout:   aws.Int64(30),
			WaitTimeSeconds:     aws.Int64(20),
		},
	}
	return &c, nil
}

func (c *Consumer) PollMessageQueue(channel chan<- *sqs.Message) {
	for {
		received, err := c.Sqs.ReceiveMessage(c.SqsReceiveParams)
		if err != nil {
			log.Fatalf("problem polling sqs: %v\n", err)
		}
		for _, message := range received.Messages {
			channel <- message
		}
	}
}

func (c *Consumer) HandleMessage(message *sqs.Message) {
	item := Item{}
	if err := json.Unmarshal([]byte(*message.Body), &item); err != nil {
		log.Fatalf("problem unmarshaling message body: %v\n", err)
	}
	log.Printf("Processing [%s]...\n", item.Name)
	w := NewWikiPage(item.Name)
	item.Links = w.Links
	item.Tags = w.Tags
	// mimic some long background process
	time.Sleep(time.Second * 10)
	// end processing
	c.UpdateItem(&item)
	log.Printf("Processing complete! Updated [%s]\n", item.Name)
}

func (c *Consumer) DeleteMessage(message *sqs.Message) {
	deleteParams := &sqs.DeleteMessageInput{
		QueueUrl:      aws.String(c.SqsQUrl),
		ReceiptHandle: message.ReceiptHandle,
	}
	_, err := c.Sqs.DeleteMessage(deleteParams)
	if err != nil {
		log.Printf("Problem deleteing message [%s]: %v", *message.MessageId, err)
	}
	log.Printf("Deleted message [%s]\n", *message.MessageId)
}

//func (c *Consumer) InsertItem(inputItemRaw *Item) {
//	inputItemMarshaled, err := dynamodbattribute.MarshalMap(inputItemRaw)
//	if err != nil {
//		log.Fatalf("Problem marshalling input-item: %s", err.Error())
//	}
//	inputItemReady := &dynamodb.PutItemInput{
//		Item:      inputItemMarshaled,
//		TableName: aws.String(c.DdbTableName),
//	}
//	// DO INSERT
//	_, err = c.Ddb.PutItem(inputItemReady)
//	if err != nil {
//		log.Fatalf("Problem inserting item into Ddb table: %s", err.Error())
//	}
//	log.Printf("Success! Inserted item [%s]\n", inputItemRaw.Name)
//}

func (c *Consumer) UpdateItem(inputItemRaw *Item) {
	// convert "metrics" map into DDB attribute
	tags, err := dynamodbattribute.MarshalMap(inputItemRaw.Tags)
	if err != nil {
		log.Fatalf("Problem marshalling metrics: %s", err.Error())
	}
	// convert "links" slice into DDB attribute
	var links []*dynamodb.AttributeValue
	for _, ln := range inputItemRaw.Links {
		lnAv := &dynamodb.AttributeValue{
			S: aws.String(ln),
		}
		links = append(links, lnAv)
	}
	// construct DDB key
	key := map[string]*dynamodb.AttributeValue{
		"name": {
			S: aws.String(inputItemRaw.Name),
		},
		//"timestamp": {
		//	S: aws.String(inputItemRaw.Timestamp),
		//},
	}
	// construct DDB update values
	update := map[string]*dynamodb.AttributeValue{
		":s": {
			S: aws.String("complete"),
		},
		":l": {
			L: links,
		},
		":t": {
			M: tags,
		},
	}
	// construct UpdateExpression
	expression := aws.String("set standing = :s, links = :l, tags = :t")
	// construct DDB Input
	inputItemReady := &dynamodb.UpdateItemInput{
		Key:                       key,
		ExpressionAttributeValues: update,
		TableName:                 aws.String(c.DdbTableName),
		UpdateExpression:          expression,
		ReturnValues:              aws.String("UPDATED_NEW"),
	}
	// DO UPDATE
	_, err = c.Ddb.UpdateItem(inputItemReady)
	if err != nil {
		log.Fatalf("Problem updating item in Ddb table: %s", err.Error())
	}
}
