### Help:

```
usage: download.py [-h]
                   (-t TITLES [TITLES ...] | -s SUBJECT | --contains CONTAINS | --regex REGEX)

optional arguments:
  -h, --help            show this help message and exit
  -t TITLES [TITLES ...], --titles TITLES [TITLES ...]
                        list of book titles to download; matches will be exact
                        (case-sensitive)
  -s SUBJECT, --subject SUBJECT
                        download books of a given subject; matches will be
                        exact (case-in-sensitive)
  --contains CONTAINS   download via substring matches on book title (case-in-
                        sensitive)
  --regex REGEX         download via regex pattern matches on book title
```

### Example usage:

```bash
python download.py -t "Handbook of the Life Course"
```

```bash
python download.py -t "Handbook of the Life Course" "Fundamentals of Power Electronics"
```

```bash
python download.py -s probability
```

```bash
python download.py --contains stochastic
```

```bash
python download.py --regex ^Brown
```
