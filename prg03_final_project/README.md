# Programming Assignment 03

## Final Project

On this 3rd (and last) programming assignment you are free to define the objectives of your data analysis, as long as the following minimum requirements are met:

* the use of Jupyter notebook as the delivery format.
* standard sections such as *preamble* with the project's title and author(s), *introduction*, *dataset*, *development*, and *conclusion*. 
* a demonstration of using of at least 5 of the following techniques:
    * data scraping 
    * API consumption 
    * summary statistics
    * data pre-processing/transformation 
    * data visualization
    * outlier analysis 
    * regression
    * classification
    * clustering
    * NLP 
    * frequent pattern mining
    * recommendation

## Ideas

There are many datasets on books that you can use as a starting point for your analysis.  For example, https://github.com/ozlerhakan/mongodb-json-files/tree/master/datasets has many datasets in JSON format, including a books.json with 431 books.  You can also try to build a more comprehensive dataset directly from https://www.goodreads.com. Once you decide which dataset to use, create a graph database on Neo4J connecting books if they share a category (or genre). Apply Louvain clustering to find book communities. Interpret the results. 

If you decide to use goodreads, you can try building a dataset of all reviews from a specific list of books. goodreads have many lists to pick here: https://www.goodreads.com/list. Some questions you may try to answer from your dataset of reviews and reviewers:

* number of reviews per rating and per genre
* geographical location of reviewers (a map visual would be nice)
* rating distribution per genre 
* outlier analysis of ratings
* sentiment analysis of the reviews 
* bag of words and bigrams of all reviews
* word cloud visualizations from reviews
* topic analysis of reviews
* pattern mining (based on the books read by reviewers, try to identify book reading patterns)

This idea can be easily adapted to other domains, such as restaurants/hotels/movies reviews, for example. Yelp and Tripadvisory are great sources for restaurants and hotel reviews. IMDb or https://www.rottentomatoes.com/ can be used for movies reviews. 

Because of privacy concerns, reviewers usually don't share much on their public profiles.  Try to create a subset of reviewers that share their *preferred genres*. Then create a recommender system based on reviewers that have similar preferred genres, recommending books that had highly positive reviews. 

## Submission

Just one members of the team (if working with a partner) needs to submit. 

If you are using Google's Colab, you can submit your project by simply sharing your notebook (read-only is fine) with your instructor (thyagomota@gmail.com). You still need to write me a comment on canvas telling me that you shared your project, listing your gmail account so I can associate the shared notebook to you. 

If you are NOT using Google's Colab, or you don't want to share through google, you can just download your notebook and upload it on canvas. 

## Rubric

\+5 for each textual (markdown) section to a max. of 25 points

\+15 for each supporting code that demonstrated required techniques used to a max. of +75 points