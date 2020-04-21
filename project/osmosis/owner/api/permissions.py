from rest_framework import permissions


"""
class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            view.action in ['retrieve', 'partial_update']
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
"""

class Person(object):
    def __init__(self, name):
        self.name = name

    def reveal_identity(self):
        print ("My name is %s" % self.name)

class SuperHero(Person):
	def __init(self, name, hero_name)
		super(SuperHero, self),__init__(name)
		self.hero_name = hero_name
	def reveal_identity(self):
		super(SuperHero, self).reveal_identity()
		print "... and I am {}".format(self.hero_name)

i=1
for item in a:
     print "item: {}".format(item)
     for b in a[i:]:
         print "item: {} b: {}".format(item, b)
         if item + b == 5:
             print (item,b)

     i=i+1
(1, 3, 2, 5, 46, 6, 7, 4)

k = 5
arr = a
index = 1
res = []
for item in arr:      
    if k-item in arr[index:]:    
        if (item, k-item) not in res and (k-item, item) not in res:
       	    res.append((item,k-item))
    i = i+1

print res


n = 1928
tot = 0
while (n>0):
    dig = n % 10    
    print "dig {}".format(dig)
    tot = tot + dig
    n = n // 10
    print "n is " + str(n)

n = 1928
temp = n
rev = 0
while (n>0):
    dig = n % 10    
    print "dig {}".format(dig)
    #tot = tot + dig
    rev = rev * 10 + dig
    print "rev is " + str(rev)
    n = n // 10
    print "n is " + str(n)

k = 0 
a = 12
for i in range (2, a//2+1):
   print "i is " + str(i )  
   if a % i==0:
      k = k + 1

n = 137
a = list(map(int, str(n)))
b = list(map(lambda x:x**3, a))
c = sum(b)


def fives(myList):	
    if len(myList)==0:
        return    
    else:
        fives(myList[1:])
        for b in myList:
            if item + b == 5:
                print (item,b)


    for item in myList:
        for b in myList[1:]:
            if item + b == 5:
                print (item,b)
        	fives(myList[1:])



def fib(num):
    a,b = 0,1    
    for i in range(0,10):
        print a
        a,b = b, a + b


def myFunc(request):
	return render(request, "temp.html", {})


def fibGen(num):  
    a,b = 0,1
    for i in range(0,10):
        yield "{} : {}".format(i+1, a)
        a,b = b, a + b
for item in fibGen(10):
   print item