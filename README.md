# QuIN

## dev venv (virtual environment) setup
- `$ python -m venv venv` (first venv indicate the venv module, second venv is the name of your virtual environment, can be anything)
- `$ venv\Scripts\activate.bat` for Windows or `vnev/bin/activate` for Linux 
- `$ pip install -r requirements.txt`
- `$ deactivate` (to exit the venv)

## image analysis projects
### interactive GUI

### curvature detection
  - progress status: on hold, minimual viable product finished
  - GUI interface for curvature detection, result stored in curvatureDetection/output_img/ and curvatureDetection/output_log
  - to run the GUI:
  1. activate venv
  2. `cd curvatureDetection`
  3. `python gui_v2.py`

### calberated resolution verification
  - progress status: on hold
  - to run exisiting code
  1. activate venv
  2. `cd imageAnalysis`
  3. `python CCD_image_analysis.py`


export new requirements
`$ pip freeze > requirements.txt`
