# gr_watcher

## Install dependencies

```bash
pipenv install --ignore-pipfile
```

To activate the virtual environment

```bash
pipenv shell
``` 

## Run

```bash
export GR_LIST=https://www.goodreads.com/review/list/74698639-ryan?shelf=test
python -m gr_watcher
```

## Prometheus

```
prometheus.yml
```

## Docker

```bash
docker build --tag gr_watcher .
docker run --env GR_LIST -d -p 5000:5000 gr_watcher
```

## Testing

Run `pytest` with coverage

```bash
pytest --cov=gr_watcher
```

```
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
gr_watcher/__init__.py                       0      0   100%
gr_watcher/__main__.py                      20     20     0%
gr_watcher/book.py                          11      0   100%
gr_watcher/bookshops/AbeBooks.py            17      0   100%
gr_watcher/bookshops/BookDepository.py      21      0   100%
gr_watcher/bookshops/Bookshop.py            40      0   100%
gr_watcher/bookshops/Waterstones.py         14      0   100%
gr_watcher/bookshops/__init__.py             0      0   100%
gr_watcher/goodreads.py                     47      0   100%
gr_watcher/utils/__init__.py                 0      0   100%
gr_watcher/utils/bcolors.py                 10      0   100%
gr_watcher/watcher.py                       53      0   100%
------------------------------------------------------------
TOTAL                                      233     20    91%
```