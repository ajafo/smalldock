__author__ = 'ajafo'


data = [1,4,2,5,6,3]
data_sort = []
for t in data:
    for d in data_sort:
        if t > d:
            data_sort.append(t)
        else:
            data_sort.index(t)
print data_sort