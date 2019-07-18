prhost='toolbarqueries.google.com'
prpath='/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'

# Function definitions
def GetHash (query):
    SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."
    Result = 0x01020345
    for i in range(len(query)) :
        Result ^= ord(SEED[i%len(SEED)]) ^ ord(query[i])
        Result = Result >> 23 | Result << 9
        Result &= 0xffffffff
    return '8%x' % Result

def GetPageRank (query):
    import http.client
    conn = http.client.HTTPConnection(prhost)
    hash = GetHash(query)
    path = prpath % (hash,query)
    conn.request("GET", path)
    response = conn.getresponse()
    data =  response.read()
    conn.close()
    data = str(bytes(data, 'utf-8'))
    print(data)
    return data.split(":")[-1]

if __name__ == "__main__" :
    a = GetPageRank("http://google.com/")
    print(a)