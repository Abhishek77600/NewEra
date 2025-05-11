# import math
# N = int(input("Enter a Number to extract digit"))
# count = 0
# cnt = int(math.log10(N)+1)
# print(cnt)
# # count = 0 
# # while(N>0):
# #     lat_digit=N%10
# #     count +=1
# #     N=N//10
# #     print(lat_digit)
# # print(count)

# def checkArmstrong(n):
#     dup = n
#     sum = 0
#     while n > 0:
#         last_digit = n%10
#         sum = sum + (last_digit*last_digit*last_digit)
#         n = n//10
#     if sum == dup:
#         return True
#     else:
#         return False

def printDivisors(n):
    for i in range(1,n+1):
      if n%i == 0:
         print(i)
printDivisors(6)