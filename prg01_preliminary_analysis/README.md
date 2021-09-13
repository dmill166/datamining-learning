# Programming Assignment 01

## Preliminary Data Analysis

In this assignment you are asked to do a preliminary data analysis of a dataset that you will build using either web scraping or API consumption techniques.  

## Requirements 

The data analysis must be presented as a Jupyter notebook with the following (required) sections: 

* Preamble: this is a markdown section containing the title of your project, author(s), contact info (email), and the date when the notebook was last updated. 
* Introduction: a short paragraph written inn markdown explaining what is your project about.
* Dataset: also in markdown, this section should describe in detail the dataset that you build for the project, explaining any specific terms related to your data collection that most people wouldn't be familiar with; if some field can be classified into categories, explain those in detail and the range of possible values for each category; describe the data collection technique used and provide links for the data source(s); describe the structure of your dataset in detail; also, this section must include the python code used for the data collection. 
* Summary Statistics: this section should present the python code that computes and prints summary statistics from your dataset, including range, mean, median, and standard deviation. 
* Visualizations: at a minimum, this section should provide 2 separate python codes, one that create a histogram and another a boxplot; the later one should also display any outliers found in the dataset. 

You are free to add other sections (those listed are the required ones). 

To be clear: you must use web scraping or API consumption to build your dataset. In other words: you are not allowed to use a dataset that is already available through download (you have to build your own dataset). 

All of the python code in the notebook must begin with a comment section like this: 

```
# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Author(s): <your name(s)>
# Description: <description>
```

## Example

Under src you can find a Jupyter notebook of an analysis of the air quality in the Denver's metro area (2020). Use it as an example of what is expected on this assignment.  

## Submission

Just one members of the team (if working with a partner) needs to submit. 

If you are using Google's Colab, you can submit your project by simply sharing your notebook (read-only is fine) with your instructor (thyagomota@gmail.com). You still need to write me a comment on canvas telling me that you shared your project, listing your gmail account so I can associate the shared notebook to you. 

If you are NOT using Google's Colab, or you don't want to share through google, you can just download your notebook and upload it on canvas. 

## Rubric

\+5 preamble section

\+10 introduction section

\+40 dataset section

    \+15 text describing the dataset

    \+25 data collection python code 

\+20 histogram data visualization (with code)

\+25 boxplot data visualization (with code and outliers computation/display)

\+10 bonus points (a 3rd data visualization of your choice)

\-5 for each source code that didn't have a comment section (as requested)