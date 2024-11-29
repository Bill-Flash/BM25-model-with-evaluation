#!/usr/bin/env python3

from files import porter
import argparse,math,os

import re

def getStopWords():
    # load stopwords into set data structure
    with open( 'files/stopwords.txt', 'r' ) as f:
        return set( f.read().split() )


def pre_process():
    ''' 1. Find all documents, and 2&3. use stopword removal, and stemming
    '''

    # step 1: extracting the documents
    filelist = os.listdir('documents') # get all names to iterate;
    N = len(filelist) # N is the total number of documents in the collection. 

    # efficient strategy: stemmed dictionary, fast to get the document length and total length for average, 
    stemmed = {} # used to efficient stemming
    lengths = {} # store the length of each documents
    total_length = 0 # store the total length of documents, and will be calculated into average
    frequencies = {} # store the number of documents containing term, and will be calculated as idf

    documents = {} # store the frequency of terms of each documents first, then will be converted into term scores

    # open document collection
    for filename in filelist:
        with open( 'documents/'+filename, 'r' ) as f:
            # use RegExpression to re.split in re third-party library
            

            # since I think space, non-letter, - and digits are something useless
            # and the query text does not contain the information that is important
            # so I decide to remove it
            terms = re.split(r'\s+|\W+|-+|\d+',f.read().lower())
            # use filter() function to filter None value
            terms = list(filter(None, terms))
            docdict = {}
            length = 0 # will be stored in the lengths later

            for term in terms:
                # stopword removal
                if term not in stopwords:
                    # effcient stemming
                    if term not in stemmed:
                        stemmed[term] = stemmer.stem(term)
                    term = stemmed[term]

                    # first time I've seen 'term' in this document
                    if term not in docdict:
                        docdict[term] = 1
                        # efficient strategy
                        # if it is the first in this document, we won't repeat the term again
                        # first time in this corpus
                        if term not in frequencies:
                            frequencies[term] = 1
                        else:
                            frequencies[term] += 1
                    else:
                        docdict[term] += 1
                    # count the length of documents
                    length += 1

            documents[filename] = docdict
            lengths[filename] = length
            total_length += length

    avg_length = int( total_length / N ) # calculate the score of 
    # strategy: It's faster than I calculate everytime in the
    # iterating the documents
    for term in frequencies:
        frequencies[term] = math.log2(  N - frequencies[term] + 0.5 ) -   math.log2( frequencies[term] + 0.5 )

    return documents, lengths, avg_length, frequencies


def indexing():
    '''using BM25 algorithm to calculate the terms in corpus
        and store it in the files/index.txt file
        
        My strategy: the weight value in the lines of the file
        is the weight score of each term in a document
    '''
    # do the pre-process first 
    documents, lengths, avg_length, idfs = pre_process()

    # calculate and store the scores
    # k and b are constants that can be set to suit the document collection
    # and the desired behaviour.
    k = 1
    b = 0.75
    # 1. calculate the BM25 score of each term in documents
    # , 2. and store them in the index.txt file
    with open('files/index.txt', 'w') as f:
        for did in documents:
            # efficient strategy here:
            # each document has its own fixed dividor, so I calculate each them before more iterations
            const_divider = k * ( ( 1 - b ) + ( ( b * lengths[did] ) / avg_length ) )
            for term in documents[did]:
                frequency = documents[did][term] 
                divider = const_divider + frequency
                score = ( frequency * ( 1 + k ) / divider ) * idfs[term]
                documents[did][term] = score
                f.write("{} {} {}\n".format( did , term , score))
    return documents

    


def load():
    '''load the index file from the local file, otherwise indexing by itself again
        The result is the the data structure that 
        a dictionary: the key is document name, and its value is another dictionary
        that uses the term as key, and the score as its value
    '''
    # judge if it exists
    if os.path.exists('files/index.txt'):
        documents = {}
        # load index from the file
        with open('files/index.txt', 'r') as f:
            for line in f:
                # format: document id; term; its score
                line = line.split(' ')
                # if the new document, create it
                if line[0] not in documents:
                    documents[line[0]] = {}

                documents[line[0]][line[1]] = float(line[2])
        return documents
    else:
        print("No index file found! Re-indexing from files, longer time....")
        return indexing()


def query(query_text, documents):
    # Query preprocess
    query_list = list()
    # lower all word case
    # split all space, non-letter, -, digits
    for term in re.split( r'\s+|\W+|-+|\d+' , query_text.lower() ) :
        if term not in stopwords and term != "":
            term = stemmer.stem(term)
            query_list.append(term)

    results = {}
    # Score calculation
    for did in documents:
        result = 0 # the score for rank
        for term in query_list:
            if term in documents[did]:
                result += documents[did][term]
        # get every document score for this query
        results[did] = result

    return results


def load_query():
    # get the queries and total number of queries from the file
    # store queries in dict, key is the QUERY ID, value is its text
    queries = {}
    number = 0
    with open( 'files/queries.txt', 'r' ) as f:
            # format: index query_text
            for query in f.read().split('\n'):
                # to skip the empty row
                if query == '':
                    continue
                query = query.split(' ',1) # one time to split index and query_text
                queries[query[0]] = query[1]
                number += 1
    return queries, number

def load_qrels():
    # give the judged-relevant/unrelevant results
    # the data structurte is a dict that use the QUERY ID as key, 
    # its value is a dict if relevant that uses the DOCUMENT ID as key, 
    # the value is its importance in that query
    # or if non-relevant that has DOCUMENT ID as a set
    relevant = {}
    with open( 'files/qrels.txt', 'r' ) as f:
            # format: index query_text
            for row in f.read().split('\n'):
                # the format is QUERYID *(ingnored) DOCUMENTID IMPORTANCE
                row = row.split()
                # it is relevant
                # first time I've seen the QUERY ID
                if row[0] not in relevant:
                    relevant[row[0]] = {}
                relevant[row[0]][row[2]] = int(row[3])
    return relevant
    
def getRetAndRel(retrieved, relevant):
    # use two list and use set to get 1 set
    return  set(retrieved).intersection(relevant)

# formula: rel&ret / ret [:15]
def get_precision(ret_rel, ret):
    return len(ret_rel)/len(ret)


# formula: rel&ret / rel
def get_recall(ret_rel, rel):
    return len(ret_rel)/len(rel)

# formula: p / n
def get_precision_at_10(retrieved, relevant):
    # top 10 results have x relevant
    # use set.intersection to find the same part
    return len(set(retrieved[:10]).intersection(relevant))/10

# formula: ret[:n]/n
def get_r_precision(retrieved, relevant):
    # top n results have x relevant
    # use set.intersection to find the same part
    len_rel = len(relevant)
    return len(set(retrieved[:len_rel]).intersection(relevant))/len_rel

def get_ap(retrieved, rel):
    # n relevant documents, find first 15 documents whether is intersected
    n = len(rel)
    ap = 0 # ap score 
    index = 1
    # iterate from the retrieved beginning due to its order, and find the first 15
    for i in range(15):
        if retrieved[i] in rel:
            ap += index/(i+1)
            index += 1
    return ap/n


def get_bpref(retrieved, relevant):
    n = len(relevant)
    non_relevant = 0
    value = 0
    # to accumulate the value 
    # until we iterats to the number of non-relevant document
    # is larger than the number of relevant document
    # reason: at this time, the bpref value will not add, and no influence
    for did in retrieved:
        # accumulate if relevant
        if did in relevant:
            value += ( 1 - ( non_relevant / n))
        else:
            non_relevant += 1
            if non_relevant >= n:
                break
    return value/n


def get_ndcg_at_n(retrieved, relevant, n):
    # NDCG @ 10 is a very commonly used metric
    sorted_relevant_list = sorted(relevant, key=relevant.get,reverse=True)[:n]
    DCG, IDCG = 0,0
    for index in range(n):
        if retrieved[index] in relevant:
            DCG += relevant[retrieved[index]] / (math.log2(index+1) if index > 0 else 1) # index = 0, divider will become 0
        # to calculate the IDCG and use if statement in case relevant less than 10
        if index < len(sorted_relevant_list):
            IDCG += relevant[ sorted_relevant_list[index] ] / (math.log2(index+1) if index > 0 else 1) # the same reason above
    
    return DCG/IDCG

def parse_args():
    '''command-line tool for getting mode'''
    # the arguments for program
    parser = argparse.ArgumentParser(description='BM25: manual/evaluation for 19206176 Qinghang Bao')
    # the mode for user to choose
    parser.add_argument('-m', '--mode', type=str, default="manual", help='Mode (manual/evaluation)',required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    # get stopwords which are both useful in manual and evaluation modes
    stopwords = getStopWords()
    

    # load the porter stemmer
    stemmer = porter.PorterStemmer()


    # stage 1: INDEXING
    print("---------This is SMALL CORPUS------------")
    print("Loading BM25 index from file, please wait.\n")
    index = load()

    if args.mode == 'manual':
        # stage 2: QUERY
        while (True): #infinite loop
            text =  input("Enter query: ")
            # if type "QUIT" program exits
            if text == "QUIT":
                print("Goodbye! :-)")
                break
            # get the retrieved results
            results =  query(text, index)
            rank = 1 # rank number
            print("Results for query [{}]".format(text))
            # print docids sorted by similarity (descending) - only show first 15
            for did in sorted( results, key=results.get, reverse=True )[:15]:
                print( '{} {} {}'.format( rank , did, results[did] ) )
                rank += 1
            print()
            
    elif args.mode == 'evaluation':
        # stage 2: Load QUERIES
        queries, query_number = load_query()
        # since small corpus only have judged documents, non-relevant can be determined by relevant
        relevant = load_qrels()

        with open( 'files/output.txt' , 'w' ) as f:
            # evaluation score initialization
            precision, recall, p_at_10, r_precision, map, bpref, ndcg = 0,0,0,0,0,0,0

            for query_id in queries:
                # get the retrieved set & sort it in a descending order
                results = query( queries[query_id] , index )
                rank_list = sorted( results, key=results.get, reverse=True )
                # get the ret&rel set, using the first 15 as usual 
                retrieved_relevant = getRetAndRel( rank_list[:15], relevant[query_id])

                precision += get_precision( retrieved_relevant, rank_list[:15] )
                recall += get_recall( retrieved_relevant, relevant[query_id] )
                p_at_10 += get_precision_at_10( rank_list, relevant[query_id] )
                r_precision += get_r_precision( rank_list, relevant[query_id])
                map += get_ap(rank_list, relevant[query_id])
                bpref += get_bpref(rank_list, relevant[query_id])
                ndcg += get_ndcg_at_n(rank_list, relevant[query_id], 10)

                rank = 1
                for did in rank_list[:15]:
                    f.write( '{} Q0 {} {} {} 19206176\n'.format( query_id, did, rank, results[did]) )
                    rank += 1
        print('Evaluation results:')
        print('Precision:    {}'.format(precision/query_number))
        print('Recall:       {}'.format(recall/query_number))
        print('P@10:         {}'.format(p_at_10/query_number))
        print('R-precision:  {}'.format(r_precision/query_number))
        print('MAP:          {}'.format(map/query_number))
        print('bpref:        {}'.format(bpref/query_number))
        print('NDCG:         {}'.format(ndcg/query_number))
                
            
            
