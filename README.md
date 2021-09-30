# Algorithm problems

- [Bucket exercise](https://github.com/dveni/algorithms/blob/main/travaso_dei_secchi.py): This implementation allows to compute the sequence of pourings given any initial state of the buckets to any given goal state of the buckets, if possible. The idea is to generate all possible future states from a specific state, saving in a dictionary only those that have not appeared before, until achieving the goal state or not having any new state (reaching the goal state from the initial state is not possible). The complexity of the path discovering algorithm is O(n^3), depending on `number of states until goal state`, `number of unexplored nodes at a specific instant` and `number of possible future states`. However, as both unexplored nodes and possible states for each node are low (<5), we could consider O(n) complexity for 3 buckets. We also assumed there are finite possible states. For example, given the initial state = (8,0,0) and the goal state = (4,4,0), the sequence would be:

  ```
  Sequence of pourings:
  A | B | C
  8 | 0 | 0
  3 | 5 | 0
  3 | 2 | 3
  6 | 2 | 0
  6 | 0 | 2
  1 | 5 | 2
  1 | 4 | 3
  4 | 4 | 0
  ```
