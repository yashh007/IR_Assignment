import re  # used for tokenization
import math  # used for logarithmic function
import nltk  # used for tokenizing queries and data
import pickle  # used for storing data into pickle files

documents = dict()  # Dictionary where (key = doc_id, value = content of documents)
inverted_index = dict()  # Dictionary where (key = word, value = list of tuples where each touple = (doc_id, freq))
doc_names = dict()  # Map of doc id to doc names



# Function to read a file where each file can have multiple documents and make the posting list
# input1 = filename to be added
# input2 = bi-word = false if uni-word indexing and true if bi-word indexing
def add_file(filename, biword=False):
    tokens = []  # list of tokens extracted from a document
    file = open(filename, mode="r", encoding="utf8")

    while (1):
        # Loop goes iterates over documents in file

        lines = []  # list of individual lines for preprocessing
        flag = 0
        while (1):
            # Loop goes over each line and breaks when end of doc is encountered thus enabling to loop over documents in the outer loop
            # If nothing is returned in read_line = end of file
            temp_line = file.readline()
            if (temp_line == ""):
                flag = 1
                break
            lines.append(temp_line)
            if (temp_line == "</doc>\n"):
                break

        if (flag):
            break

        doc_id = int(lines[0].split("\"")[1])
        doc_title = (lines[0].split("\"")[5])
        # print(doc_title)
        doc_names[doc_id] = doc_title

        # Goes over each line once again to remove hyper-links. ***Can be done in the first loop
        for idx in range(len(lines)):
            lines[idx] = lines[idx].replace('&quot;', '"')  # Removing an abnormality found in the corpus
            # line = re.sub(r'<doc id="([0-9]*)" url=".*" title="(.*)">', r"id=\1\n \2 titend\n", text)
            lines[idx] = re.sub('<[^>]*>', '', lines[idx])  # Remove hyperlinks in each line
        # print(lines)

        # Makes a string appending all lines so that it can be fed to nltk
        data = " ".join(lines[1:])  # Adds the lines first line onwards
        documents[doc_id] = data
        tokens = get_tokens(data, biword=biword)
        update_inverted_index(doc_id, tokens)

    print("Documents Indexed")

    file.close()



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



# Function to add tokens in the posting list
# input1 = documentID of the document that is tokenized and to be stored into the posting list
# input2 = list of tokens created from the data in the document represented by the documentID
def update_inverted_index(doc_id, tokens):
    # Function updates the inverted index for each document
    for word in tokens:
        if word in inverted_index:
            if inverted_index[word][-1][0] == doc_id:
                inverted_index[word][-1] = (doc_id, inverted_index[word][-1][1] + 1)
            else:
                inverted_index[word].append(tuple([doc_id, 1]))
        else:
            inverted_index[word] = [(doc_id, 1)]




# Main code = driver code to call the sequence of functions

print("Do you want index to be Bi-word or Uni-word ?? [B/U]") # asking for type of indexing
flag = input()

# making posting list
print("Making posting list!!")
if (flag=="B")|(flag=="b"): # if indexing is Bi-word or not
    add_file("wiki_92", biword= True)
else:
    add_file("wiki_92",biword = False)

print("posting list made!!")
print("storing in pickle files!!")

# converting to pickle objects and storing in pickle files
f1 = open("inverted_index.pickle" , "wb")
f2 = open("document_id_document_title.pickle" , "wb")
f3 = open("document_data.pickle" ,"wb")
pickle.dump(inverted_index,f1,protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(doc_names,f2,protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(documents,f3,protocol=pickle.HIGHEST_PROTOCOL)

print("Posting list stored successfully!!")
# closing files
f1.close()
f2.close()
f3.close()

# end of the code