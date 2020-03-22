package main

import (
	"encoding/json"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/sqs"
	"log"
	"os"
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
	ddbSess, err := session.NewSession(&aws.Config{
		Region:   aws.String("us-east-1"),
		Endpoint: aws.String("http://aws-stack:4564"),
	})
	if err != nil {
		return nil, err
	}
	sqsSess, err := session.NewSession(&aws.Config{
		Region:   aws.String("us-east-1"),
		Endpoint: aws.String("http://aws-stack:4576"),
	})
	if err != nil {
		return nil, err
	}
	queueUrl := os.Getenv("AWS_SQS_QUEUE_URL")
	c := Consumer{
		Ddb:          dynamodb.New(ddbSess),
		DdbTableName: os.Getenv("AWS_DDB_TABLE_NAME"),
		Sqs:          sqs.New(sqsSess),
		SqsQUrl:      queueUrl,
		SqsReceiveParams: &sqs.ReceiveMessageInput{
			QueueUrl:            aws.String(queueUrl),
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
			log.Fatalf("Problem receiving message: %s", err.Error())
		}
		for _, message := range received.Messages {
			channel <- message
		}
	}
}

func (c *Consumer) HandleMessage(message *sqs.Message) {
	item := Item{}
	if err := json.Unmarshal([]byte(*message.Body), &item); err != nil {
		log.Fatalf("Problem unmarshaling message body: %s", err.Error())
	}
	log.Printf("Attempting to process and update item!\n")
	// todo: processing here
	w := NewWikiPage(item.Name)
	item.Links = w.Links
	// end processing
	c.UpdateItem(&item)
}

func (c *Consumer) DeleteMessage(message *sqs.Message) {
	deleteParams := &sqs.DeleteMessageInput{
		QueueUrl:      aws.String(c.SqsQUrl),
		ReceiptHandle: message.ReceiptHandle,
	}
	_, err := c.Sqs.DeleteMessage(deleteParams)
	if err != nil {
		log.Printf("Problem deleteing message [%s]: %s", *message.MessageId, err.Error())
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
	// key item
	//inputItemMarshaled, err := dynamodbattribute.MarshalMap(inputItemRaw)
	//if err != nil {
	//	log.Fatalf("Problem marshalling input-item: %s", err.Error())
	//}

	var links []*dynamodb.AttributeValue
	for _, ln := range inputItemRaw.Links {
		lnAv := &dynamodb.AttributeValue{
			S: aws.String(ln),
		}
		links = append(links, lnAv)
	}

	key := map[string]*dynamodb.AttributeValue{
		"name": {
			S: aws.String(inputItemRaw.Name),
		},
		//"timestamp": {
		//	S: aws.String(inputItemRaw.Timestamp),
		//},
	}
	// updated item
	update := map[string]*dynamodb.AttributeValue{
		":s": {
			S: aws.String("complete"),
		},
		":l": {
			L: links,
		},
		":empty_list": {
			L: []*dynamodb.AttributeValue{},
		},
	}
	inputItemReady := &dynamodb.UpdateItemInput{
		Key:                       key,
		ExpressionAttributeValues: update,
		TableName:                 aws.String(c.DdbTableName),
		UpdateExpression:          aws.String("set standing = :s, links = list_append(if_not_exists(links, :empty_list), :l)"),
		ReturnValues:              aws.String("UPDATED_NEW"),
	}
	// DO UPDATE
	_, err := c.Ddb.UpdateItem(inputItemReady)
	if err != nil {
		log.Fatalf("Problem updating item in Ddb table: %s", err.Error())
	}
	log.Printf("Success! Updated item [%s]\n", inputItemRaw.Name)
}
