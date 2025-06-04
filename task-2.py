def binary_search(array: list[float], value: float) -> tuple[int, float]:
  start_index = 0
  end_index = len(array) - 1
  iter_count = 0
  upper_bound = float('inf')
  
  while start_index <= end_index:
    iter_count += 1
    mid_index = (start_index + end_index) // 2
    mid_value = array[mid_index]
      
    if value < mid_value:
      upper_bound = mid_value
      end_index = mid_index - 1
    elif value > mid_value:
      start_index = mid_index + 1
    else:
      return (iter_count, mid_value)

  
  return (iter_count, upper_bound if upper_bound != float('inf') else -1)

array = [1.1, 2.2, 3.3, 4.4, 5.5]
value = 3.0
result = binary_search(array, value)
print(result)