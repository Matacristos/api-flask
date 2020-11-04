Flask basic server

### Run in local

1. Install pipenv

    * sudo apt-get update
    * sudo apt-get install pipenv

2. Run: 
    
    * pipenv shell
    * pipenv install

3. Run:
    * pipenv run python3 init.py

### Run with Docker

1. Build image: `docker build -t api-flask .`
2. Run container: `docker run -p 5000:5000 api-flask`
 * With volume: `docker run -p 5000:5000 -v "$(pwd):/app" api-flask`

### Dataset generation
__The csv has a header row__, be careful
- `src/coindesk.py populate` to populate data csv
- `src/coindesk.py update` to update with latest data
- `src/coindesk.py check` to check diff between dates

* Alternative dataset with script: 
- `src/bitflyer.py` to populate data csv

## Train model from scratch

`pipenv shell`

Open the Python terminal and run:

```
from model import get_model
from train import train

model = get_model()
train(csv_path='./data/bitcoin.new.csv', model=model, num_epochs=50)

model.save('./models/model.h5')
```
