import re
import nltk
import ftfy
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

common_re = re.compile(r"[*].+[*]") #remove ******* This Lyrics is NOT for Commercial use *******
punt_re = re.compile(r"[^a-zA-Z' ]+") #irrelevant puctuations
tokenise_re = re.compile(r"(\[[^\]]+\]|[-'\w]+|[^\s\w\[']+)") #([]|words|other non-space)

def preprocess(text):
    text = text.lower()
    p_text = common_re.sub("", text)
    p_text = punt_re.sub("", p_text)
    p_text = ftfy.fix_text(p_text)
    return p_text.lower()  #return lyrics in the same case

def replace_apostrophe(lyrics):
    full_text = ""
    tokens = lyrics.split(" ")
    for text in tokens:
        if "'" in text:
            shortened = text.split("'")
            if shortened[1] == "ll" or text == "i\'mma":
                text = shortened[0] + " will"
            elif shortened[1] == "m":
                text = shortened[0] + " am"
            elif shortened[1] == "d" or text == "'d":
                text = shortened[0] + " would"
            elif shortened[1] == "ve":
                text = shortened[0] + " have"
            elif shortened[1] == "s":
                text = shortened[0] + "s"
            elif shortened[1] == "re":
                text = shortened[0] + " are"   
            elif text == "\'cause" or shortened[1] == "cause" or text == "\'cuz":
                text = "because"
            elif shortened[1] == "" or shortened[0][-2:] == "in":
                text = shortened[0] + "g"
            elif text == "y\'all":
                text = "you all"
            elif text == "\'em" or text == " 'em":
                text = "them"
            elif text == "\'lone":
                text = "alone"
            elif text == "c\'mon":
                text = "common"
            elif shortened[1] == "t" and shortened != "ain":
                text = shortened[0] + " not"
        full_text = full_text + " " + text
    return full_text       
     
def tokenise(text):
    return tokenise_re.findall(text)

def remove_stopwords(tokens):
    nltk_filtered = [word for word in tokens if word not in stop_words]
    return nltk_filtered

def frequency_analysis(tokens):
    freq = nltk.FreqDist(tokens)
    for key,val in freq.most_common(20):
        print(key,val,sep="\t")
    freq.plot(20, cumulative=False)