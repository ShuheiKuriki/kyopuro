# A,B=int(input()),int(input(),base=2)
# print(">"if A>B else("<"if A<B else"="))

A = input()
B = int(input(),base=2)
if len(A)>=2000:exit(print(">"))
A = int(A)
print(">"if A>B else("<"if A<B else"="))