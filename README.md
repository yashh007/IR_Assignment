TITLE :- IR Assignment 1
Date :- 1st May 2021

Authors :- 
           ARYAN GUPTA        2018A7PS0017P
           AARNAV DHANUKA     2017B5A70945P
           YASH AGRAWAL       2018A7PS0251P
           AHMAD FARAZ        2017B4A70558P
           SUJEET SRIVASTAVA  2017A4PS0503P


CONTENTS :- 
           REPORT          = contains the results and summary of the IR model
           indexer.py      = python file that reads wiki_92 and creates a posting list and stores the posting lists in pickle files
           test_queries.py = python file that reads the pickle files and ask queries and rerieve relevant documents 
           wiki_92         = corpus used by the IR model for document retrieval 



HOW TO RUN CODE :-

    1) Run the indexer.py file
       In command line write "python3 indexer.py" 
    2) The terminal asks a question about the type of indexing to be done(biword or uniword)
    3) Input B for Biword and U for uniword indexing
    4) After entering the index wait for the python code to store data in the pickle files
       and successfull msg will appear

    -> You have successfully created the posting list and stored in 3 files 

    5) To run the model run test_queries.py 
       In command line write "python3 test_queries.py"
    6) The terimanl asks for wether title weighting needs to be done or not
    7) Input Y if terminal weighting needs to be done and N if not 
    8) The model then asks for queries that you need to search
    9) The model outputs 10 documents for each query with their rank , id , title ,score

    -> keep quering the model as long as you want

    10) To end the model just input exit instead of query to exit the model .



CODE DESCRIPTION ->

1)indexer.py ->

   1.1)Data Structures ->

         a) inverted_index (dictionary) :- used to store a list of tokens mapped to a list of(documentID , termfrequecy)
         b) documents(dictionary) :- used to store docID and their corresponding data 
         c) doc_names(dictionary) :- used to store DocID and their corresponding titles
   
   1.2)Functions ->

         a) add_file -> used to read a file and update the posting list accordingly
            1) It starts reading the file .
            2) Loops through each line read and using get_tokens converts data int tokens 
            3) for each document one entry in doc_names and documents is also done 
            4) using update_inverted_index posting list is updated .

         b) get_tokens -> used to convert input string to tokens 
            1) uses nlt.word_tokenise function to tokenise the input string 
            2) removes all special characters and lower cases every token 
            3) if biword indexing is done all tokens are then changed to tuples of biwords
            4) the list of tokens are returned
         
         c) update_inverted_index -> used to update inverted index 
            1)it iterated through the list of tokens 
            2) for each token a new entry (docID,1) is made if that document is not in the list 
            3) if the document is in the list the corresponding term frequency is increased

   1.3)Main Code -> driver code that calls all the functions sequentially

      1) asks wether biword indexing is to be done or not 
      2) the choice is then read by input() function 
      3) if choice is B the biword indexing is done else uni-word 
      4) all the three datstructures are then stroed into 3 pickle files using pickle.dump:-
         inverted_index.pickle <- store inverted_index
         document_id_document_title.pickle <- store doc_names 
         document_data.pickle <- store documents
      5) files are closed and the indexing is completed 



2)test_queries.py :-

   2.1)Data Structures :-
         
         a) inverted_index (dictionary) :- used to store a list of tokens mapped to a list of(documentID , termfrequecy)
         b) documents(dictionary) :- used to store docID and their corresponding data 
         c) doc_names(dictionary) :- used to store DocID and their corresponding titles

   2.2)Functions :-

      a) get_tokens -> used to convert input string to tokens 
         
         1) uses nlt.word_tokenise function to tokenise the input string 
         2) removes all special characters and lower cases every token 
         3) if biword indexing is done all tokens are then changed to tuples of biwords
         4) the list of tokens are returned

      b) normalize_vector -> used to normalise input dictionary 
         
         1) iterates thru the input dictionary and add the square of each value
         2) devide each value in dictionary woth the total sum of sqaures

      c) calculate_ltc_query -> convert input query into normalised vector 

         1)query is changed to lit of tokens using get_tokens
         2)for each token in query their term frequencies are stored in query_tf
         3)for each token their document frequency is calculated but taking their length of posting list 
         4)the token document frequency is stored in query_df 
         5)for each entry in query_df we use (1+log(n/df)) to convert to idf values
         6)then by taking the vector product of the two dictionary we get the unnormalised final vector 
         7)by passing this vector to normalize_vector we finally get the normalized ltc vector which is returned 

      d) calculate_lnc_document -> calculates lnc vector for each document in the corpus 

         1) the inverted_index is iterated and vectors for each document are created consisting of the tokens and their term frequency .
         2) then all the document are normalized using normalise_vector
         3) then the dictionary of document vectors are returned 

      e) calculate_scores -> calculates lnc.ltc similarity scores for each document wrt query

         1) dot product of query vector and each document vector is done 
         2) the corresponding result for eah document is stroed in a dictionary named scores 
         3) the scores dictionary is then returned

      f) find_top_k_results -> give top k documents which have the best scores 

         1) the scores dictionary is then coverted to list of tuples (score,doc_id)
         2) the list is then sorted in revere order
         3) the firs k documents are then printed

      g) query_processor -> prints top k documents for an input query 

         1) query ltc vector is made by using the calculate_ltc_query
         2) document vectors are found by using calculate_lnc_document
         3) scores for each document are found by calculate_scores
         4) using the scores top k documents are printed using find_top_k_results

      h) title_weighting -> adds title weighting to the position list(inprovemet 2)

         1) iterate thru all the doc_names dictionary
         2) and for each title convert into tokens using get_tokens
         3) for each token scale up the its term frequency of the corresponding document 
         4) if that token is in tiltle but not in data add (Docid,10) to the tokens posting list 

   2.3) Main function :- driver code 

      1) it opens all the three pickle files where the posting list and other dat structures are stored 
      2) it then checks weither the indexing is biword or uniword and updates the variable biword True or False respectively
      3) it then asks if title weighting needs to be done 
      4) if Y is given as input then title_weighting function is called 
      5) it then keeps on asking queries and then for each query results are shown as query_processor
      6) if exit is given as input the programme ends .



