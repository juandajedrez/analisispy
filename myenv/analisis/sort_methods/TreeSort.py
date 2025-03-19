from pybtex.database import parse_file, BibliographyData
import time

class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


def insert(root, key):
    if root is None:
        return TreeNode(key)

    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    return root


def inorder_traversal(root, res):
    if root:
        inorder_traversal(root.left, res)
        res.append(root.val)
        inorder_traversal(root.right, res)


def tree_sort(arr):
    if not arr:
        return arr

    root = None
    for key in arr:
        root = insert(root, key)

    sorted_arr = []
    inorder_traversal(root, sorted_arr)
    return sorted_arr


# Example usage
#arr = [5, 3, 7, 2, 8, 1, 4, 6]
#sorted_arr = tree_sort(referencias)
#print("Sorted array:", sorted_arr)

