package main

// an incoming item from the queue
type Item struct {
	Timestamp string 	`json:"timestamp"`
	Name      string    `json:"name"`
	Standing    string    `json:"standing"`
}

// contains fields to be updated
type ItemUpdated struct {
	Standing    string    `json:":s"`
}
