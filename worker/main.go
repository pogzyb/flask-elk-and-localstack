package main

import (
	"./scraper"
	"github.com/aws/aws-sdk-go/service/sqs"
	"log"
)

func main() {
	messageChannel := make(chan *sqs.Message, 3)

	c, err := scraper.New()
	if err != nil {
		log.Fatalf("Got error: %s", err.Error())
	}

	go c.PollMessageQueue(messageChannel)

	for msg := range messageChannel {
		log.Println("Got a message!", msg)
		c.HandleMessage(msg)
		c.DeleteMessage(msg)
	}
}
