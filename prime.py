n=int(input("enter range:"))

isPrime=[True]*(n+1)
isPrime[0]=isPrime[1]=False
for i in range (2,n+1):
    if isPrime[i]:
        for j in range(i*i,n+1,i):
            isPrime[j]=False
print([i for i in range(n + 1) if isPrime[i]])