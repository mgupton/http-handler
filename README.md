# http-handler
http-handler is basic HTTP server.

```
python http-handler.py
```

```
curl -X POST -d "Hello World!" http://localhost
````

## Result

```
Handling request

----- Request Start ----->

/
Host: localhost
User-Agent: curl/7.50.1
Accept: */*
Content-Length: 12
Content-Type: application/x-www-form-urlencoded


Hello World!
<----- Request End -----

127.0.0.1 - - [06/Mar/2017 13:13:37] "POST / HTTP/1.1" 200 -
```