package main

// an incoming item from the queue
type Item struct {
	ID          int              `json:"id"`
	DateAdded   string           `json:"date_added"`
	DateUpdated string           `json:"date_updated"`
	Term        string           `json:"term"`
	Standing    string           `json:"standing,omitempty"`
	Links       []string         `json:"links,omitempty"`
	Tags        map[string]int64 `json:"tags,omitempty"`
}

// contains fields to be updated
//type ItemUpdated struct {
//	Standing string   `json:":s"`
//	Links    []string `json:":l"`
//}
