import hashlib


class TaoGeKey:
    def __init__(self, key):
        self.key:str = key

    def encodeText(self, text):
        hashCode = int(hashlib.sha256(self.key.encode("utf-8")).hexdigest(), 16)
        result = b""
        for i in text:
            byte = i.encode("utf-8")
            if hashCode%255 == 0:
                hashCode = hashCode + 1
            for j in range(len(byte)):
                result += ((byte[j] + abs(hashCode)) % 255).to_bytes(1, byteorder="big")
        ans = ""
        for i in result:
            ans = ans + chr(i)
        return ans

    def decodeText(self, text):
        hashCode = int(hashlib.sha256(self.key.encode("utf-8")).hexdigest(), 16)
        result = b""
        for i in text:
            tem = ord(i) - abs(hashCode) % 255
            if (tem < 0):
                tem = 255 + tem
            result += tem.to_bytes(1, byteorder="big")
        return result.decode("utf-8")


if __name__ == "__main__":
    taoge = TaoGeKey("111111")
    print(taoge.decodeText("%Ç¾#ùã%ÆÏ'ý×#öè'¿È$âç$ìâ'ýÖ%Öí%ÚÇ&À÷&Òæ&ØÂ$ÎåH"))
