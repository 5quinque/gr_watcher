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

## Testing

Run `pytest` with coverage

```bash
pytest --cov=gr_watcher
```
