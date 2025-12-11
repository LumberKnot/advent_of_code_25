## Cashing as speedup

This library can be used to very easiely add a cache to the program. The n-ple `(input1, intput2, ...)` must be hashable i.e no lists. _I think_ value must be singular but not sure.

```python
from functools import cache

@cache
def function(input1, input2, ...) -> value
```

## Realy ought to learn some more common algorithms

...and where to use them.

Where I have noticed to be lacking is

- Graphs
- System of equations
