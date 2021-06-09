# legisCrawler: An Automation Webcrawling Toolkit for Taiwan Parliamentary Questions

An automation web crawling framework for retrieving parliamentary questions on The Website of Taiwan Legislative Yuan 立法院 (https://lis.ly.gov.tw/) based on Selenium library in Python and Chrome browser. 


<p align="center">
  <img width="700" height="500" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image1.png" >
</p>


## Requirements

- python>=3.7.3 🐍
- pip>=19.2
- numpy=1.16.2
- pandas=0.24.2
- matplotlib=3.0.3
- selenium
- webdriver-manager

## Instruction

- Need to install [Anaconda Navigator](https://www.anaconda.com/products/individual-b) and [Python>=3.7.3](https://www.python.org/downloads/release/python-3810/) beforehand. And then, open the terminal and download `legisCrawler` repository by using `git clone`(about how to use git and Github, please have a look at this [Tutorial for Beginners](https://www.youtube.com/watch?v=RvnM6EEwp1I) )
```
git clone  git@github.com:davidycliao/legisCrawler.git
```

- Copy and paste the commands as below:
```
# Change the directory by typing `cd` command once `legisCrawler` repository is downloaded.
cd legisCrawler
# Create the enviroment by using conda and name the enviroment as `legisCrawler`.
conda create -n legisCrawler python=3.7 
# Activate the pre-named enviroment. 
conda activate legisCrawler 
# Install the dependencies from `requirements.txt` using `pip` methond.
pip install -r requirements.txt   
```

- When **legisCrawler** is running, you will be asked which term (2nd - 10th) you would like to scrape (please, type any single digit from 2 to 10). Then **legisCrawler** will automatically create a folder to restore the retrieval of parliamentary questions by the individual legislators.  


## Workflow 

<p align="center">
  <img width="700" height="220" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image4.png" >
</p>


## What **legisCrawler** Scrapes
This designed crawler automatically webscrapes the parliamentary questions (專案質詢) from The Website of Legislative Yuan, including a bunch of information with regards to the topic, keywords and the type. An additional module for getting a corpus of grand parliamentary debates (總質詢) is in progress and will be available soon.

<p align="center">
  <img width="700" height="500" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image3.png" >
</p>


## Note
If there’s anything you need about the application, please don’t hesitate to send me a message in [Discussion](https://github.com/davidycliao/legisCrawler/discussions) 📣. 


## Cite

For citing this work, you can refer to the present GitHub project. For example, with BibTeX:
```
@misc{legisCrawler,
    howpublished = {\url{https://github.com/davidycliao/PorkCNN}},
    title = {An Automation Webcrawling Toolkit for Taiwan Parliamentary Questions},
    author = {David, Yen-Chieh Liao and Calvin, Yu-Ceng Liao},
    publisher = {GitHub},
    year = {2021}
}
```

