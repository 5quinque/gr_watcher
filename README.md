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
gr_watcher/GoodReads.py                     50      6    88%
gr_watcher/__init__.py                       0      0   100%
gr_watcher/__main__.py                      18     18     0%
gr_watcher/bookshops/AbeBooks.py            16      3    81%
gr_watcher/bookshops/BookDepository.py      19      6    68%
gr_watcher/bookshops/Bookshop.py            41      5    88%
gr_watcher/bookshops/BookshopOld.py         24     24     0%
gr_watcher/bookshops/Waterstones.py          9      0   100%
gr_watcher/bookshops/__init__.py             0      0   100%
gr_watcher/data/__init__.py                  0      0   100%
gr_watcher/utils/__init__.py                 0      0   100%
gr_watcher/utils/bcolors.py                 10      0   100%
gr_watcher/watcher.py                       39     11    72%
------------------------------------------------------------
TOTAL                                      226     73    68%
```