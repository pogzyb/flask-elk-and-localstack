package main

import (
	"golang.org/x/net/html"
	"io"
	"log"
	"net/http"
	"strings"
)

type WikiPage struct {
	Term    string
	Tags	map[string]int64
	Links   []string
}

func NewWikiPage(term string) *WikiPage {
	tags := make(map[string]int64)
	w := WikiPage{Term: term, Tags: tags}
	page := getPage(w.Term)
	w.parseWikiPage(&page)
	return &w
}

func replaceWhiteSpaces(term string) string {
	return strings.Replace(term, " ", "_", -1)
}

func getPage(term string) io.Reader {
	termUnderScored := replaceWhiteSpaces(term)
	wikiURL := "https://wikipedia.org/wiki/" + termUnderScored
	response, err := http.Get(wikiURL)
	if err != nil {
		log.Printf("bad response wikipedia: %v", err)
	}
	//log.Println("Got response status code: ", response.StatusCode)
	return response.Body
}

func (w *WikiPage) parseWikiPage(Html *io.Reader) {
	iterTokens := html.NewTokenizer(*Html)
	for {
		it := iterTokens.Next()
		switch it {
		case html.StartTagToken:
			w.handleStartTag(iterTokens)
		case html.ErrorToken:
			return
		}
	}
}

func (w *WikiPage) handleStartTag(tokenizer *html.Tokenizer) {
	tag, hasAttr := tokenizer.TagName()
	tagString := string(tag)
	_, exists := w.Tags[tagString]
	if !exists {
		w.Tags[tagString] = 1
	} else {
		w.Tags[tagString] += 1
	}
	if tagString == "a" && hasAttr {
		w.handleHrefAttr(tokenizer)
	}
}

func (w *WikiPage) handleHrefAttr(tokenizer *html.Tokenizer) {
	attr, value, more := tokenizer.TagAttr()
	// check for href and if href starts with "/" or "http"
	attrStr := string(attr)
	if attrStr == "href" {
		if strings.HasPrefix(attrStr, "/") || strings.HasPrefix(attrStr, "http") {
			w.Links = append(w.Links, string(value))
		}
	}
	if more {
		w.handleHrefAttr(tokenizer)
	}
}
