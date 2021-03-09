# https://discuss.leetcode.com/topic/81637/two-solutions-and-thoughts
import string, random

class Codec:
    dic = string.ascii_letters+'0123456789'
    basicUrl = 'http://tinyurl.com/'

    def __init__(self):
        self.url2code = {}
        self.code2url = {}

    def encode(self, longUrl):
        """Encodes a URL to a shortened URL.
        
        :type longUrl: str
        :rtype: str
        """
        while not longUrl in self.url2code:
            code = ''.join(random.choice(self.dic) for _ in range(6))
            if not code in self.code2url:
                self.url2code[longUrl] = code
                self.code2url[code] = longUrl
        return self.basicUrl + self.url2code[longUrl]

        

    def decode(self, shortUrl):
        """Decodes a shortened URL to its original URL.
        
        :type shortUrl: str
        :rtype: str
        """
        return self.code2url[shortUrl[-6:]]
        

url = 'https://leetcode.com/problems/design-tinyurl'

codec = Codec()
shortUrl = codec.encode(url) 
print shortUrl
print codec.decode(shortUrl)
