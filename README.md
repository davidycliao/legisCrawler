# legisCrawler: An Automation Webcrawling Toolkit for Taiwan Parliamentary Questions

An automation web crawling framework for retrieving parliamentary questions on The Website of Taiwan Legislative Yuan 立法院 (https://lis.ly.gov.tw/) based on Selenium library in Python and Chrome browser. 


<p align="center">
  <img width="700" height="500" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image1.png" >
</p>


## Requirements
- python>=3.7.3
- pip>=19.2
- numpy=1.16.2
- pandas=0.24.2
- matplotlib=3.0.3
- selenium
- webdriver-manager

## Installation Instruction

- Need to install [Anaconda Navigator](https://www.anaconda.com/products/individual-b) and [Python>=3.7.3](https://www.python.org/downloads/release/python-3810/) 🐍 beforehand.

- Open the terminal and down load this repository by typing the command as below:
```
git clone  git@github.com:davidycliao/legisCrawler.git
```
- Once the repository is download, you should change the directory using `cd` command.
```
cd legisCrawler
```

- Create the enviroment by using conda and I name enviroment as `legisCrawler`.
```
conda create -n legisCrawler python=3.7      
```

- Activate the pre-named enviroment. 

```
conda activate legisCrawler                 
```
- Install the dependencies packages using `pip` methond.

```
pip install -r requirements.txt             
```
- Last, run the `legisCrawler` in the terminal. 
```
python legisCrawler.py
```


## Workflow in the **legisCrawler**

<p align="center">
  <img width="700" height="220" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image4.png" >
</p>


## What **legisCrawler** Scrapes
This designed crawler automatically webscrapes the parliamentary questions (專案質詢) from The Website of Legislative Yuan, including a bunch of information with regards to the topic, keywords and the type. 
<p align="center">
  <img width="700" height="500" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image3.png" >
</p>


- When **legisCrawler** is running, you will be asked which term (2nd - 10th) you would like to scrape (please, type digit number from 2 o 10). Then **legisCrawler** will automatically create a folder to restoring the parliamentary questions by the individual legislators.  

## Note
If there’s anything you need about the application and end-to-end use, please don’t hesitate to send me a message in [Discussion](https://github.com/davidycliao/legisCrawler/discussions) 📣. 



