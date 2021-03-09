class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        if nums1 == [] and nums2 == []:
            return 0

        if nums1 == []:
            return (nums2[(len(nums2)-1)/2]+nums2[len(nums2)/2])/2.
        if nums2 == []:
            return (nums1[(len(nums1)-1)/2]+nums1[len(nums1)/2])/2.
        minv = min(nums1[0],nums2[0])
        maxv = max(nums1[-1],nums2[-1])
        nums10 = [minv]
        nums10.extend(nums1)
        nums10.append(maxv)
        nums20 = [minv]
        nums20.extend(nums2)
        nums20.append(maxv)
        nums1 = nums10
        nums2 = nums20

        def swap(a,b):
            return b,a

        def swapAll(s1,s2,i,j,lefti,leftj,righti,rightj):
            s1, s2 = swap(s1,s2)
            i ,j = swap(i,j)
            lefti, leftj = swap(lefti,leftj)
            righti,rightj = swap(righti,rightj)
            return s1,s2,i,j,lefti,leftj,righti,rightj

        def check(s1,s2,i,j,lefti,leftj,righti,rightj,needTwo,target):
            if i+j+1 == target:
                if i == len(s1)-1 or s1[i+1] >= s2[j]:
                    if needTwo:
                        if j == 0 :
                            self.re = (s2[j]+s1[i-1])/2.
                        else:
                            self.re = (s2[j]+max(s1[i],s2[j-1]))/2.
                    else:
                        self.re = s2[j]
                    return False
            return True

        i,j = (len(nums1)-1)/2, (len(nums2)-1)/2
        self.re = 0
        lefti = 0
        leftj = 0
        righti = len(nums1)
        rightj = len(nums2)
        needTwo = (len(nums1)+len(nums2))%2 == 0
        target = (len(nums1)+len(nums2))/2
        re = 0
        s1 = nums1
        s2 = nums2

        if s1[i] > s2[j]:
            s1,s2,i,j,lefti,leftj,righti,rightj = swapAll(s1,s2,i,j,lefti,leftj,righti,rightj)

        while check(s1,s2,i,j,lefti,leftj,righti,rightj,needTwo,target):
            if (i+j+1) == target:
                rightj = j+1
                j = (j+leftj)/2
                lefti = i
                i = (i+righti)/2
            else:
                if (i+j+1) > target:
                    rightj = j+1
                    j = (j+leftj)/2

                else:

                    lefti = i
                    i = (i+righti)/2

            if s1[i] > s2[j]:
                s1,s2,i,j,lefti,leftj,righti,rightj = swapAll(s1,s2,i,j,lefti,leftj,righti,rightj)

        return self.re

s = Solution()

num1 = [8,9]
num2 = [1,2,3,4,5,6,7,10]

print s.findMedianSortedArrays(num1,num2)


# https://discuss.leetcode.com/topic/22406/python-o-log-min-m-n-solution
# class Solution:
#     # @return a float
#     def findMedianSortedArrays(self, A, B):
#         l=len(A)+len(B)
#         return self.findKth(A,B,l//2) if l%2==1 else (self.findKth(A,B,l//2-1)+self.findKth(A,B,l//2))/2.0


#     def findKth(self,A,B,k):
#         if len(A)>len(B):
#             A,B=B,A
#         if not A:
#             return B[k]
#         if k==len(A)+len(B)-1:
#             return max(A[-1],B[-1])
#         i=len(A)//2
#         j=k-i
#         if A[i]>B[j]:
#             #Here I assume it is O(1) to get A[:i] and B[j:]. In python, it's not but in cpp it is.
#             return self.findKth(A[:i],B[j:],i)
#         else:
#             return self.findKth(A[i:],B[:j],j)