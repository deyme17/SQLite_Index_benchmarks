# SQLite Index Benchmarks

## Overview

This project benchmarks SQLite query performance on large datasets with different indexing strategies for 2D coordinate data.  
It focuses on measuring query execution time for rectangular range queries on `x` and `y` fields, comparing:

- No index
- Single index on `x`
- Single index on `y`
- Composite index on `(x, y)`
- Using two separate indexes combined with `INTERSECT`


## Reference

This benchmark is inspired by and related to the research on using SQLite for spatial data storage:

SQLite as a Spatial Data Store
https://www.researchgate.net/publication/348558938_SQLite_KAK_HRANILISE_PROSTRANSTVENNYH_DANNYH