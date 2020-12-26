package main

import (
	"github.com/aws/aws-sdk-go/service/sqs"
	"log"
)

func main() {
	// unbuffered channel to handle completion
	done := make(chan struct{})

	// buffered channel to handle incoming messages
	messageChannel := make(chan *sqs.Message, 3)

	// init new "Consumer"
	c, err := New()
	if err != nil {
		log.Fatalf("error trying to init consumer: %v\n", err)
	}

	//
	go c.PollMessageQueue(messageChannel)

	for msg := range messageChannel {
		log.Println("Got a message!", msg)
		go func(message *sqs.Message) {
			c.HandleMessage(message)
			c.DeleteMessage(message)
		}(msg)
	}
	<- done
}
