Flask basic server

1. Install pipenv

    * sudo apt-get update
    * sudo apt-get install pipenv

2. Run: 
    
    * pipenv install

3. Run:
    * pipenv run python3 init.py
    

### Dataset generation
__The csv has a header row__, be careful
- `src/coindesk.py populate` to populate data csv
- `src/coindesk.py update` to update with latest data