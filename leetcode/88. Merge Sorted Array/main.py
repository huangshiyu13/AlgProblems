class Solution:
    def merge_my(self, nums1, m, nums2, n: int):
        n1 = m-1
        n2 = n-1
        index_now = m+n-1
        while n1 >= 0 or n2 >= 0:
            if n1 < 0:
                nums1[:n2+1] = nums2[:n2+1]
                return
            else:
                if n2 < 0:
                    return
                else:
                    if nums1[n1] < nums2[n2]:
                        nums1[index_now] = nums2[n2]
                        n2-=1
                    else:
                        nums1[index_now] = nums1[n1]
                        n1-=1
                    index_now-=1

    def merge_my(self, nums1, m, nums2, n: int):
        index_now = m+n-1
        while m > 0 and n > 0:
            n1 = m-1
            n2 = n-1
            if nums1[n1] < nums2[n2]:
                nums1[index_now] = nums2[n2]
                n-=1
            else:
                nums1[index_now] = nums1[n1]
                m-=1
            index_now-=1
        if n > 0:
            nums1[:n] = nums2[0:n]