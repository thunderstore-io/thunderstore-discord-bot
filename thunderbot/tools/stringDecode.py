import base64

def base64_decode(bs64str):
    message_bytes = base64.b64decode(bs64str)
    decodeStr = message_bytes.decode('ascii')
    return decodeStr
