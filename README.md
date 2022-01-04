### Requirements
 - Python 3 (tested on 3.9.7)
 - installed `requirements.txt`


### Run tests

```shell
make test
```

### Run `invaders` lib with sample data

```shell
make run-sample
```


### General description

Provided solution is based on three objects types:
 - `Shape` – it is a thin wrapper around 2d array, intended to hold loaded space and invaders
 - `ScoreEngine` – defines basic interface for calculating similarity scoring for any point of the
    space and an invader
 - `Detector` –  given `Shapes` of the space and an invader crawls the space and invokes 
   `ScoreEngine` either for all points of the space or only for most promising (depending 
  on implementation).


#### Sample data

The solution is intended to be re-usable collection of classes, `run_sample.py` is exemplary usage 
of the library with sample data and is not in a strict way part of the solution.

Values of `detected_invader_min_score` and `fill_ratio_max_diff` parameters used in `run_sample.py` 
have been adjusted to yield most accurate results or at least perceived as such by the author 
of the solution.
