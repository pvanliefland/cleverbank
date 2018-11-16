# cleverbank
A quick data test

To run it with docker, clone, cd and:

```bash
docker build -t cleverbank .
docker run -v ${PWD}:/usr/src/app cleverbank
```

If you have Python 3 installed on your local machine, just clone, cd and run:

```bash
python report.py
```

The report file will be written to `data/bankreport.txt`.