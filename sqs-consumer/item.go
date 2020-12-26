package main

// an incoming item from the queue
type Item struct {
	Timestamp string           `json:"timestamp"`
	Name      string           `json:"name"`
	Standing  string           `json:"standing"`
	Links     []string         `json:"links,omitempty"`
	Tags   map[string]int64    `json:"tags,omitempty"`
}

// contains fields to be updated
//type ItemUpdated struct {
//	Standing string   `json:":s"`
//	Links    []string `json:":l"`
//}
