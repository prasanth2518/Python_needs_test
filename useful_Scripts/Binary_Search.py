'''
Binary Search Applys On only the list is Sorted one
Here we will take the middle value and Find the value in the list

'''


def Binary_Search(lst, key):
    low = 0
    high = len(lst) - 1
    Found = False
    while low <= high and not Found:
        mid = (low + high) // 2
        if key == lst[mid]:
            Found = True
        elif key > lst[mid]:
            low = mid + 1
        else:
            high = mid - 1
    if Found:
        print("key is found")
    else:
        print("key is not found")


lst = [37, 53985, 3689, 5e2434, 7299]
lst.sort()
key = int(input("Enter Key: "))
Binary_Search(lst, key)
