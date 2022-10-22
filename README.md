# Analysis-Tools [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg) [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nathanw23-analysis-tools-streamlit-appapp-ewjbas.streamlitapp.com/)

### Description
A suite of command line tools for plotting and analysing data obtained from a Clariostar plate reader, Cary Eclipse spectrophotometer, and Nanodrop 2000c. 

### Installation
To install, *ideally* create a new environment using your preferred Python environment manager:

```conda create -n analysis_tools python=3.8```

Then install the required packages as follows:

1. ```pip install -r requirements.txt```

2. ```pip install -e .```

Once installed, the tools can be used from any location on your computer. 

Tested using Python 3.8 on Windows 10 and Mac OS 12.6

### Usage

 - All available tools and a brief description can be found by entering ```analysis_tools``` 
 - Program specific information can be found by typing ```--help``` after the program name

### Updating

After updating the repo (```git pull```), update the command line interface using ```pip install -e .``` at the repo root directory
