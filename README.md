# COMP3009J – Information Retrieval Programming Assignment
### Author
Qinghang Bao 
### UCD Student Number
19206176
## Programming Assignment

My program can run both small and large corpus. Besides, I write two .py files for each corpus. 
This file describes what this program can do and how to run it. (assuming that the program will be run in the same directory as the README.md file (i.e. the current directory will have the [documents](documents) and [files](files) directories in it).)

### What this program can do
This is a standalone program on the command line, and can do the following things:

##### Select Mode
* select the mode (manual/evaluation) to query or evaluate this model

##### BM25 IR model
* index the small corpus, and large corpus, and store it named ``index.txt`` (in the [files](files) directory).
* load the index from the ``index.txt`` file, if it already has been created.
* respond to a query by using BM25 IR model

##### Evaluation
* use the standard queries that are read from the [queries.txt](files/queries.txt) and part of the corpus provided to evaluate the effectiveness of the BM25 approach.
* create ``output.txt`` (in the [files](files) directory) to store the responses. 
* return a list of the 15 most relevant documents, sorted beginning with the highest similarity score (format: the rank, the document’s ID, and the similarity score).
* calculate and print the average evaluation metrics score (based on the relevance judgments contained in the ``qrels.txt`` file in the ``files`` directory)
* Metrics: Precision, Recall, P@10, R-precision, MAP, bpref, NDCG

### How to run it
#### Small corpus
If users want to enter queries manually, they should be able to run (assuming your program is called search.py):

``python search_small.py -m manual``

And then, just need to type the text you want query.

Or to run the evaluations:

``python search_small.py -m evaluation``
***
#### Large corpus
If users want to enter queries manually, they should be able to run (assuming your program is called search.py):

``python search_large.py -m manual``

And then, just need to type the text you want query.


Or to run the evaluations:

``python search_large.py -m evaluation``

***
####Q&A
**Q1:** What if it tells me the problem of import error.

```
Traceback (most recent call last):
File "search_xx.py", line 3, in <module>
    from files import porter
ImportError: No module named files
```
**A1:** The python version is innerly defined as python2. Please transform it into ``python3 xxx``
