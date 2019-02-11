Lab 1 (counts as 50% of Homework 1): Data processing with pandas
UIC CS 418, Spring 2019

The following three steps should have been completed before the lab (as instructed last week). 
If you haven't completed them before coming to class today, you will need to complete them now before you can proceed with the actual lab instructions.
If you have completed them, you can skip the three steps and proceed to =LAB INSTRUCTIONS=:

1. Install anaconda 2018.12 for python 3.7.1: https://www.anaconda.com/download
If you already have anaconda, make sure it's updated to this version:

elena-macbook$ conda update conda
elena-macbook$ conda install anaconda=2018.12

2. In your terminal, check whether you have the right anaconda version:

elena-macbook$ conda --version
conda 4.5.12

If the command cannot be found, then make sure you have closed and re-opened the terminal window after installing it.

3. Check your Python version

elena-macbook$ python --version
Python 3.7.1 :: Anaconda, Inc.

If it does not show Python 3.7.1, make sure Python 3.7.1 is installed.

=================== LAB INSTRUCTIONS ==========================

Move lab1.zip to your CS 418 homework directory (e.g., cs418-hw) and unzip it.

Create a python 3.7.1 environment (very important!):

elena-macbook:cs418-hw elena$ conda create -n cs418env python=3.7.1 anaconda

Activate the environment:

elena-macbook:cs418-hw elena$ source activate cs418env   #omit the source part on windows

Change to lab directory:

(cs418) elena-macbook:cs418-hw elena$ cd lab1

Start the Jupyter notebook:

(cs418) elena-macbook:lab1 elena$ jupyter notebook &

This should open a notebook in your web browser and display the contents of the current directory. Select lab1.ipynb, and follow the instructions in the notebook.



