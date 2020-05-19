class Solution:
    def largestPerimeter(self, A) -> int:
        A.sort(reverse=True)
        for i in range(0, len(A)):
            if (A[i] < A[i - 1] + A[i - 2]):
                return A[i] + A[i - 1] + A[i - 2]
        return 0

    def maxProfit(self, prices) -> int:
        risingIntervals = []
        i = 0
        while i < len(prices):
            RI = [i]
            for j in range(i + 1, len(prices)):
                if (prices[j] < prices[i] or prices[j] < prices[j - 1]):
                    RI.append(j - 1)
                    i = j - 1
                    break
                elif (j == len(prices) - 1):
                    RI.append(j)
                    i = j
                    break
                else:
                    pass
            i += 1
            risingIntervals.append(RI)
        P = 0
        for i in range(0, len(risingIntervals)):
            risingIntervals[i] = list(set(risingIntervals[i]))
            risingIntervals[i].sort()
            if len(risingIntervals[i]) == 2:
                P += (prices[risingIntervals[i][1]] - prices[risingIntervals[i][0]])
        return P, risingIntervals

    def compress(self, chars):
        i = 0
        length = len(chars)
        while i < length:
            char = chars[i]
            count = 1
            j = i + 1
            while j < length:
                if chars[j] == char:
                    count += 1
                    del chars[j]
                    length = len(chars)
                else:
                    break
            if (count >= 2):
                for each in str(count):
                    chars.insert(i + 1, each)
                    i += 1
            else:
                i += 1
            length = len(chars)
        return length

    def isHappy(self, n: int) -> bool:
        loop_detect = [n]
        while n != 1:
            s = str(n)
            n = 0
            for digit in s:
                n += int(digit) ** 2
            if n in loop_detect:
                return False
            loop_detect.append(n)
        return True

    MapDict = {
        0: 0,
        1: 1,
        2: 5,
        3: None,
        4: None,
        5: 2,
        6: 9,
        7: None,
        8: 8,
        9: 6
    }

    def rotateThisNumber(self, N):
        N = str(N)
        T = ""
        for digit in N:
            if self.MapDict[int(digit)]:
                T += str(self.MapDict[int(digit)])
            else:
                return False
        if T == N:
            return False
        else:
            return True

    def rotatedDigits(self, N: int) -> int:
        count = 0
        for i in range(1, N + 1):
            if self.rotateThisNumber(i):
                count += 1
        return count

    def detectCapitalUse(self, word: str) -> bool:
        hasLower = False
        for i in range(0,len(word)):
            c = word[i]
            hasLower = hasLower or c.islower()
        for i in range(0,len(word)):
            c = word[i]
            if c.isupper() and i!=0 and hasLower:
                return False
        return True


S = Solution()
print(S.detectCapitalUse("FFFFFFFFFFFFFFFFFFFFf"))
