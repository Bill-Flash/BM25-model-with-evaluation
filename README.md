# BM25 implemetation and their evaluation
### Author
Bill-Flash

Please contact me through Issues if you need the data.

## Programming

My python program can run both small and large corpus. Besides, I write two .py files for each corpus. 
This file describes what this program can do and how to run it. (assuming that the program will be run in the same directory as the README.md file (i.e. the current directory will have the [documents](documents) and [files](files) directories in it).)

### What this program can do
This is a standalone program on the command line, and can do the following things:

##### Select Mode
* select the mode (manual/evaluation) to query or evaluate this model

# **BM25 Strategies Summary**

## **Preprocessing Strategies**

1. **Stopword Removal**  
   - Loaded a list of common stopwords from `stopwords.txt` and filtered them out during document and query preprocessing to reduce noise.

2. **Stemming**  
   - Used the Porter Stemmer to reduce words to their root forms (e.g., "running" → "run").
   - Cached stemmed terms in a dictionary to avoid redundant stemmer calls, improving efficiency.

3. **Tokenization and Filtering**  
   - Split document text into tokens using a regex (`\s+|\W+|-+|\d+`) to clean the text by removing spaces, non-letters, digits, and hyphens.  
   - Filtered out empty tokens using Python’s `filter()` function.

4. **Document Length Optimization**  
   - Calculated and stored each document’s length and the total length of all documents during preprocessing.  
   - Precomputed the average document length (`avg_length`) to avoid recalculating it during BM25 scoring.

5. **Term Frequency and Document Frequency Calculation**  
   - Counted term frequencies for each document.  
   - Calculated document frequencies (number of documents containing each term) and precomputed inverse document frequency (IDF) values for efficient scoring.

---

## **BM25 Scoring Strategies**

1. **Precomputed Constants**  
   - Used constants `k = 1` and `b = 0.75` to adjust term importance based on frequency and document length.

2. **Efficient Divisor Calculation**  
   - Precomputed the divisor for each document (`const_divider`) to minimize redundant calculations during BM25 scoring.

3. **Score Calculation for Terms**  
   - Used the BM25 formula:  

     \[
     \text{Score} = \frac{f \cdot (k+1)}{f + k \cdot (1-b + b \cdot \frac{L}{\text{avg\_length}})} \cdot \text{idf}
     \]

     Where:  
     - \( f \): Term frequency in the document.  
     - \( L \): Document length.  
     - \( \text{idf} \): Inverse document frequency.

4. **Indexing**  
   - Stored BM25 scores for terms in each document in an `index.txt` file for later retrieval.  
   - Each line in the file stores the **document ID**, **term**, and **BM25 score**, ensuring efficient loading and querying.

---

## **Querying Strategies**

1. **Preprocessing Queries**  
   - Applied the same **stopword removal**, **stemming**, and **tokenization** strategies to query terms to ensure consistency with document preprocessing.

2. **Query Scoring**  
   - Scored each document for a query by summing the BM25 scores of query terms present in the document.  
   - Sorted documents by their scores in descending order to retrieve the most relevant results.

3. **Top-K Results**  
   - Limited the number of results displayed to the **top 15 documents** for efficiency during ranking and evaluation.

---

## **Evaluation Strategies**

1. **Loading Relevance Judgments**  
   - Loaded relevance judgments from `qrels.txt`, storing them as a dictionary where each query ID maps to relevant document IDs and their relevance scores.

2. **Evaluation Metrics**  
   - Implemented the following metrics to evaluate the system's performance:
     - **Precision**: Proportion of retrieved documents that are relevant.  
     - **Recall**: Proportion of relevant documents that are retrieved.  
     - **Precision@10**: Precision for the top 10 retrieved documents.  
     - **R-Precision**: Precision at the number of relevant documents for a query.  
     - **MAP (Mean Average Precision)**: Average precision across all retrieved relevant documents.  
     - **BPref**: A preference-based evaluation metric that rewards ranking relevant documents higher than non-relevant ones.  
     - **NDCG@10 (Normalized Discounted Cumulative Gain)**: Evaluates ranking quality, giving higher importance to highly relevant documents.

3. **Batch Evaluation**  
   - Processed all queries from `queries.txt` and calculated metrics for each query.  
   - Averaged metrics across all queries to provide overall performance scores.

4. **Output Results**  
   - Stored evaluation results and ranked retrieval results in an output file (`output.txt`), formatted for easy inspection and debugging.

## How to run it
### Small corpus
If users want to enter queries manually, they should be able to run (assuming your program is called search.py):

``python search_small.py -m manual``

And then, just need to type the text you want query.

Or to run the evaluations:

``python search_small.py -m evaluation``
***
### Large corpus
If users want to enter queries manually, they should be able to run (assuming your program is called search.py):

``python search_large.py -m manual``

And then, just need to type the text you want query.


Or to run the evaluations:

``python search_large.py -m evaluation``

***
#### Q&A
**Q1:** What if it tells me the problem of import error.

```
Traceback (most recent call last):
File "search_xx.py", line 3, in <module>
    from files import porter
ImportError: No module named files
```
**A1:** The python version is innerly defined as python2. Please transform it into ``python3 xxx``
