from hashlib import md5

if __name__ == "__main__":
    key = "ckczppom"
    zeros = 6

    i = 0
    while True:
        attempt = "".join([key, str(i)]).encode('utf-8')
        if md5(attempt).hexdigest()[0:zeros] == "0" * zeros:
            print(i)
            break
        i += 1