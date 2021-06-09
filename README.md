# legisCrawler: An Automation Webcrawling Toolkit for Taiwan Parliamentary Questions

An automation web crawling framework for retrieving parliamentary questions on The Website of Taiwan Legislative Yuan 立法院 (https://lis.ly.gov.tw/) based on Selenium library in Python and Chrome browser. 


<p align="center">
  <img width="700" height="500" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image1.png" >
</p>



## Requirements
- python=3.7.3
- pip=19.0
- numpy=1.16.2
- pandas=0.24.2
- matplotlib=3.0.3
- selenium
- webdriver-manager

## Installation
- Suggest to use [Anaconda Navigator](https://www.anaconda.com/products/individual-b) and [Python 3.8.1](https://www.python.org/downloads/release/python-3810/) 🐍 .
- Install [ChromeDriver 91.0.4472.19](https://sites.google.com/chromium.org/driver/downloads) in working directory. 
- Suggest installing the packages mentioned above via importing `webscrae_env.yml` in `Anaconda Navigator` or build up the environment by inserting `requirements.txt` using conda. 

## Workflow in the **legisCrawler**

<p align="center">
  <img width="700" height="220" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image4.png" >
</p>


## What **legisCrawler** Scrapes
This designed crawler automatically webscrapes the parliamentary questions (專案質詢) from The Website of Legislative Yuan, including a bunch of information with regards to the topic, keywords and the type. 
<p align="center">
  <img width="700" height="500" src="https://raw.githack.com/davidycliao/legisCrawler/main/images/image3.png" >
</p>

## Instruction

- Download the repository or importing a Git repository using the command line, see [GitHub Doc](https://docs.github.com/en/github/importing-your-projects-to-github/importing-source-code-to-github/importing-a-git-repository-using-the-command-line).

```
$ git clone --bare git@github.com:davidycliao/legisCrawler.git
# 
Makes a bare clone of the external repository in a local directory
```
- You will need to install [chromedriver](https://chromedriver.chromium.org/downloads) in your working directory to run legisCrawler.
- Run it in the terminal via the environment set up via `Anaconda Navigator`.
- Run `python legisCrawler.py` in your terminal command line 


- When **legisCrawler** is running,  you will be asked which term (2nd - 10th) you would like to scrape. Then **legisCrawler** will automatically create a folder for restoring the parliamentary questions by the individual legislators.  

## Note
If there’s anything you need about the application and end-to-end use, please don’t hesitate to send me a message in [Discussion](https://github.com/davidycliao/legisCrawler/discussions) 📣. 



