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
gr_watcher/__main__.py                      18     18     0%
gr_watcher/book.py                          11      0   100%
gr_watcher/bookshops/AbeBooks.py            17      0   100%
gr_watcher/bookshops/BookDepository.py      21      2    90%
gr_watcher/bookshops/Bookshop.py            42      3    93%
gr_watcher/bookshops/Waterstones.py         10      0   100%
gr_watcher/bookshops/__init__.py             0      0   100%
gr_watcher/goodreads.py                     50      6    88%
gr_watcher/utils/__init__.py                 0      0   100%
gr_watcher/utils/bcolors.py                 10      0   100%
gr_watcher/watcher.py                       45      4    91%
------------------------------------------------------------
TOTAL                                      224     33    85%
```