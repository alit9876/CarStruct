

def linear_search(cars, key, field):
    """
    Perform linear search on the given list of cars based on the specified field.
    :param cars: List of Car objects
    :param key: Value to search for
    :param field: Field to search in (e.g., 'price', 'mileage', etc.)
    :return: List of cars matching the search criteria
    """
    results = []
    for car in cars:
        if getattr(car, field) == key:
            results.append(car)
    return results


def binary_search(cars, key, field):
    """
    Perform binary search on the given sorted list of cars based on the specified field.
    :param cars: Sorted list of Car objects
    :param key: Value to search for
    :param field: Field to search in (e.g., 'price', 'mileage', etc.)
    :return: List of cars matching the search criteria
    """
    low, high = 0, len(cars) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = getattr(cars[mid], field)

        if mid_value == key:
            return [cars[mid]]

        elif mid_value < key:
            low = mid + 1

        else:
            high = mid - 1

    return []


def quicksort(cars, field='price'):
    """
    Perform quicksort on the given list of cars based on the specified field.
    :param cars: List of Car objects
    :param field: Field to sort on (default is 'price')
    :return: Sorted list of cars
    """
    if len(cars) <= 1:
        return cars

    pivot = getattr(cars[len(cars) // 2], field)
    left = [car for car in cars if getattr(car, field) < pivot]
    middle = [car for car in cars if getattr(car, field) == pivot]
    right = [car for car in cars if getattr(car, field) > pivot]

    return quicksort(left, field) + middle + quicksort(right, field)


def merge_sort(cars, field='price'):
    """
    Perform merge sort on the given list of cars based on the specified field.
    :param cars: List of Car objects
    :param field: Field to sort on (default is 'price')
    :return: Sorted list of cars
    """
    if len(cars) <= 1:
        return cars

    # Split the list in half
    mid = len(cars) // 2
    left_half = cars[:mid]
    right_half = cars[mid:]

    # Recursively apply merge sort on each half
    left_half = merge_sort(left_half, field)
    right_half = merge_sort(right_half, field)

    # Merge the sorted halves
    return merge(left_half, right_half, field)


def merge(left, right, field):
    """
    Merge two sorted lists based on the specified field.
    :param left: Left sorted list
    :param right: Right sorted list
    :param field: Field to compare (e.g., 'price', 'mileage', etc.)
    :return: Merged sorted list
    """
    result = []
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        if getattr(left[left_index], field) < getattr(right[right_index], field):
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]

    return result
