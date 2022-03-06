def merge_sort(lst, comparator=min):

    if len(lst) == 1:
        return lst
        
    mid_way = len(lst) // 2
    a = lst[:mid_way]
    b = lst[mid_way:]
    
    a_sorted = merge_sort(a, comparator)
    b_sorted = merge_sort(b, comparator)
    
    merge_sorted = merger(a_sorted, b_sorted, comparator)
    
    return merge_sorted
    
def merger(a, b, comparator):
    sorted_ = []
    
    while a and b:
        element_1 = a[0]
        element_2 = b[0]
        
        result = comparator(element_1, element_2)
        sorted_.append(result)
        if result == element_1:
            del a[0]
        else:
            del b[0]
    
    while a:
        sorted_.append(a[0])
        del a[0]
        
    while b:
        sorted_.append(b[0])
        del b[0]
        
    return sorted_
    
x = list(range(9, 0, -1))
print(merge_sort(x))