import usocket
import ujson

class Response:

    def __init__(self, s):
        self.socket = s
        self.encoding = "utf-8"
        self._header = None
        self._content = None
        
        header = str(s.readline(), "utf-8")
        l = header.split(" ")
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()
        #print(status, reason)
        
        self._status_code = status
        self._reason = reason
        while True:
            x = s.readline()
            if not x or x == b"\r\n":
                break
            header = header + str(x, "utf-8")
            if x.startswith(b"Transfer-Encoding:"):
                if b"chunked" in x:
                    raise ValueError("Unsupported " + x)
            elif x.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
        
        self._header = header
        self._content = str(self.socket.recv(4096), self.encoding)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
        self._content = None
        
    @property
    def header(self):
        return self._header
    
    @property
    def content(self):
        return self._content

    @property
    def status_code(self):
        return self._status_code

    @property
    def reason(self):
        return self._reason

    def json(self):
        c = self._content
        if (c is None):
            return None
        else:
            return ujson.loads(c)


def request(method, url, data=None, json=None, headers={}, stream=None):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    
    s = usocket.socket()

    
    #try:
    s.connect(usocket.getaddrinfo(host, port)[0][-1])

    if port == 443:
        s = ussl.wrap_socket(s, server_hostname=host)
    s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
    if not "Host" in headers:
        s.write(b"Host: %s\r\n" % host)
    # Iterate over keys to avoid tuple alloc
    for k in headers:
        s.write(k)
        s.write(b": ")
        s.write(headers[k])
        s.write(b"\r\n")
        
    if json is not None:
        assert data is None
        import ujson
        data = ujson.dumps(json)
        
        s.write(b"Content-Type: application/json\r\n")
    if data:
        s.write(b"Content-Length: %d\r\n" % len(data))
    s.write(b"\r\n")
    if data:
        s.write(data)
    

    resp = Response(s)
    return resp


def head(url, **kw):
    return request("HEAD", url, **kw)

def get(url, **kw):
    return request("GET", url, **kw)

def post(url, **kw):
    return request("POST", url, **kw)

def put(url, **kw):
    return request("PUT", url, **kw)

def patch(url, **kw):
    return request("PATCH", url, **kw)

def delete(url, **kw):
    return request("DELETE", url, **kw)



