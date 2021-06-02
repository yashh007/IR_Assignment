import math # use math.log function for calculating logarithms
import pickle # to read pickle files and import posting list
import nltk  # fro tokenization of title weighting is done

documents = dict() # Dictionary where (key = doc_id, value = content of documents)
inverted_index = dict() # Dictionary where (key = word, value = list of tuples where each touple = (doc_id, freq))
doc_names = dict() # Map of doc id to doc names



# Function to tokenize text
# input1 = string that needs to be tokenized
# input2 = bi-word = True if bi-word indexing is done else false in uni-word indexing is being done
# output = returns the list of tokens extracted from the input string
def get_tokens(text, biword=False):
    # Function return tokens from a string input(text)

    punct_set = {"\n", "``", "''", ".", ",", "(", ")", "-", "–", "—", ";", ":", "[", "]", "'", "...", "!", "?", "#",
                 "$", "%", "&", "*", "+", "--", "/", "=", ">", "@", "{", "}", "~", "`", "|"}

    tokens = nltk.word_tokenize(text)
    tokens = [word.lower() for word in tokens if
              word not in punct_set]  # Removes punctuation marks and makes all tokens lower case

    if (biword):
        biwords = list(nltk.bigrams(tokens))
        # print(type(biwords[0]))
        tokens.extend(biwords)

    return tokens


# Function to normalize vectors
# input = dictionary representing a vector
# output = input dictionary vector after normalization
def normalise_vector(vector):
    #Function takes a vector as an input and returns it after normalization
    temp = 0

    for i in vector:
        # summing up all the squares
        temp += vector[i]*vector[i]
    if temp==0:
        return vector

    for i in vector:
        # normalizing the vector
        vector[i] = vector[i]/temp

    return vector


# function to make ltc vector of query
# input1 = query that needs to be vectorized
# input2 = bi-word = True if bi-word indexing is done and False if uni-word indexing
def calculate_ltc_query(query, biword):
    #Function takes query as input and returns ltc vector of the query
    tokens = get_tokens(query, biword = biword)

    # query_tf stores the query vector tf values
    query_tf = {}
    # calculating tf of each token present in the query
    for i in tokens:
        query_tf[i] = query_tf.get(i, 0)+1
    for i in query_tf:
        query_tf[i] = (1+math.log(query_tf[i]))

    # query_df stores the query vector df values
    query_df = {}
    global inverted_index

    for i in query_tf:
        try:
            query_df[i] = len(inverted_index[i])
            continue
        except:
            # if there is no entry in corpus of that token that token need not be taken in the final query vector
            continue


    # calculating idf using query_df
    global doc_names
    n = len(doc_names)
    for i in query_df:
        query_df[i] = math.log(n/query_df[i])

    # query vector contains the final vector to be returned
    query_vector = {}
    for i in query_tf:
        try:
          query_vector[i] = query_tf[i] * query_df[i]  # vector = tf*idf
        except:
          continue

    query_vector = normalise_vector(query_vector)
    return query_vector

# function to make lnc vector of all documents
def calculate_lnc_document():
    # calculates lnc vector for all documents
    global inverted_index

    # document_tf contains key = doc_id and value as lnc vector
    document_tf = {}
    # creating doc id = 1 + log(tf) mapping
    for i in inverted_index:
        for j in inverted_index[i]:
            document_tf[j[0]] = document_tf.get(j[0], {})
            document_tf[j[0]][i] = 1 + math.log(j[1])

    #normalizing all the vectors
    for i in doc_names:
        document_tf[int(i)] = normalise_vector(document_tf[int(i)])

    return document_tf


# calculates scores for every document
# input1 = query vector of the model
# input2 = document vectors needed for score calculation
def calculate_scores(query , document):
    scores = {}
    for i in document:
        doc_vector = document[i]
        score = 0
        for j in query:
            try:
                score += query[j] * doc_vector[j]
                continue
            except:
                continue
        scores[i] = score
    return scores

# Function outputs top k document their scores and their titles
# input1 = scores = dictionary of having all scores of documents
# input2 = k = no. of documents to be printed
def find_top_k_results(scores , k):

    # ls is temp list containing (score,doc id) tuple
    ls = []
    for i in scores:
        ls.append((scores[i],i))
    # sorting ls in descending order
    ls.sort(reverse=True)
    global doc_names
    #printing results
    for i in range(k):
        print("Rank:-", i+1, "Doc ID->", ls[i][1], ",Title:->",doc_names[ls[i][1]],  ",Score:->", ls[i][0])


# Main Model function that calls all the functions sequentially to make the code work
def query_processor(query, k = 10, biword = False):
    # Function takes query as input and prints the top 5 documents as search results
    query = calculate_ltc_query(query, biword)
    lnc = calculate_lnc_document()
    scores = calculate_scores(query, lnc)
    find_top_k_results(scores, k)

# Function representing improvemet-2 where posting list updated and term frequencies are scaled up if a token appears in its title
def title_weighting(biword = False):
    # Function increases the frequency of title words in document to increase words in the title
    global inverted_index, doc_names
    scale = 1000 # Factor to scale up by
    print("title weighting done")
    for doc_id in doc_names:
        tokens = get_tokens(doc_names[doc_id], biword)

        for token in tokens:
            flag1 = 0  # flag is set if the corresponding document was found in the token
            flag2 = 0  # flag2 is set if there is no entry of the token in the title
            for temp in range(len(inverted_index.get(token,[]))):
                flag2=1
                if inverted_index[token][temp][0] == int(doc_id):
                    #inverted_index[token][temp][1] += 10
                    inverted_index[token][temp] = (int(doc_id), inverted_index[token][temp][1]*scale)
                    flag1 = 1
                    break
            if flag2==0:
                inverted_index[token] = []
            if flag1 == 0:  # flag = 0 means no entry was found
                inverted_index[token].append((int(doc_id), 10))


# Reading pickle files and importing the posting list
f1 = open("inverted_index.pickle" , "rb")
f2 = open("document_id_document_title.pickle" , "rb")
f3 = open("document_data.pickle" ,"rb")
documents = pickle.load(f3)
doc_names = pickle.load(f2)
inverted_index = pickle.load(f1)

if(type(list(inverted_index.keys())[-100])==str):
    indexing = False
else:
    indexing = True
#print(indexing)
# main code

print("Do you want title weighting or not??[Y/N]")# Y fro yes and N for No
c = input()
if((c=="Y")|(c=="y")):
    title_weighting()
while(1):
    print("Enter query to search, exit to stop")
    query = input()
    if query == "exit":
        break
    query_processor(query , biword=indexing)


