# QuIN
## image analysis project
- curvature detection
  - activate venv
  - `cd imageAnalysis`
  - `python pixis_analysis.py` (in development)
- calberated resolution verification
  - activate venv
  - `cd imageAnalysis`
  - `python CCD_image_analysis.py` (in development)
## dev venv setup
- `$ python -m venv venv` (first venv indicate the venv module, second venv is the name of your virtual environment, can be anything)
- `$ venv\Scripts\activate.bat` for Windows or `vnev/bin/activate` for Linux 
- `$ pip install -r requirements.txt`
- `$ deactivate` (to exit the venv)

export new requirements
`$ pip freeze > requirements.txt`
