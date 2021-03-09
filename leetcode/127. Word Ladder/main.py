import collections

class Solution(object):
    def constructDic(self, wordList):
        dic = collections.defaultdict(list)

        for word in wordList:
            for i in range(len(word)):
                key = word[:i]+'_'+word[i+1:]
                dic[key].append(word)
        return dic

    def ladderLength(self, beginWord, endWord, wordList):
        if not endWord in wordList: return 0

        dic = self.constructDic(wordList)

        headVisited, tailVisited = set(),set()
        headVisited.add(beginWord)
        tailVisited.add(endWord)

        words1, length1 = [beginWord],1
        words2, length2 = [endWord],1

        while words1 and words2:
            next_words = []
            if len(words1) <= len(words2):
                for word in words1:
                    for i in range(len(word)):
                        key = word[:i]+'_'+word[i+1:]
                        for next_word in dic[key]:
                            if next_word not in headVisited:
                                if next_word in words2:
                                    return length1+length2
                                headVisited.add(next_word)
                                next_words.append(next_word)
                words1 = next_words
                length1 = length1+1
            else:
                for word in words2:
                    for i in range(len(word)):
                        key = word[:i]+'_'+word[i+1:]
                        for next_word in dic[key]:
                            if next_word not in tailVisited:
                                if next_word in words1:
                                    return length1+length2
                                tailVisited.add(next_word)
                                next_words.append(next_word)
                words2 = next_words
                length2 = length2+1

        return 0

s = Solution()

beginWord = "hot"
endWord = "dog"
wordList = ["hot","dog"]
print s.ladderLength(beginWord, endWord, wordList)