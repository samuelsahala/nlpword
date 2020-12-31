# nlpword

Word frequency implemented with Trie algorithm.
The app is capable of receiving three types of input, simple string, Url or a file 
and allows you to count the frequency usage of each word in your text.(Language Processing)

### File Structure ( The important ones :) )
```
.nlpword
├── flask - main folder
│   ├── app
│   │    └── static
│   │        └── template (templete for easy testing, 
│   │            ├── main page - inputs
│   │            ├── success.html - results
│   │            ├── ws.html - search
│   │        └── helper.py (all they helper function generic split, create trie store
│   │        └── main.py (main routes - /submit-string , /submit-url, /submit-file)
│   └── env
│   └── app.py - running the app.
├── nginx
```

### General guidelines of the process 
[![Untitled-Diagram.png](https://i.postimg.cc/Y9BgD0km/Untitled-Diagram.png)](https://postimg.cc/4KwmmJYJ)

