# QuIN
This repository records my ongoing work at the QuIN research lab in the University of Waterloo as a undergraduate research assistant. For more information about the research group, please visit the lab [website](https://research.iqc.uwaterloo.ca/quinkim/research/).

## dev virtual environment setup (python venv) 
- `$ python -m venv venv` (first venv indicate the venv module, second venv is the name of your virtual environment, can be anything)
- `$ venv\Scripts\activate.bat` for Windows or `vnev/bin/activate` for Linux 
- `$ pip install -r requirements.txt`
- To exit the venv run `$ deactivate`

## image analysis projects
### interactive GUI
- project status: IN PROGRESS

to run the GUI:
1. activate venv
2. `cd gui`
3. `python app.py`
<img width="512" alt="image" src="https://github.com/Huan-YiShen/QuIN/assets/76965211/ec9f2065-dd8f-4e39-bb80-4de83b7e3ade">

### curvature detection
  - progress status: on hold, minimual viable product finished
  - GUI interface for curvature detection, result stored in curvatureDetection/output_img/ and curvatureDetection/output_log


to run the GUI:
  1. activate venv
  2. `cd curvatureDetection`
  3. `python gui_v2.py`

<img width="447" alt="image" src="https://github.com/Huan-YiShen/QuIN/assets/76965211/a151c7b8-4df9-4b55-b02d-0d58bdef4e03">


### calberated resolution verification
  - progress status: on hold
  - to run exisiting code
  1. activate venv
  2. `cd imageAnalysis`
  3. `python CCD_image_analysis.py`


## Maintainer note
- when adding new requirements to the venv, be sure to record it in the requirements.txt `$ pip freeze > requirements.txt`
- once a proejct or GUI is finished, use [pyinstaller](https://pyinstaller.org/en/stable/) or equvalent library to bundle it into a executable 
