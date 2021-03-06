# a driver for our summarizer.
# authors: Kirsten Vail, Derek Palinski, Lee Schumann

from nltk.corpus import reuters
from summarizer import Summarizer
import random
import paragraphs


def main():
    # create our summarizer
    cfs = Summarizer()
    getSummaries(cfs, 2)

def getSummaries(cfs, number_of_summaries):
    for n in range(number_of_summaries):
        # get a random article from the corpus
        article = random.choice(reuters.fileids())
        # make sure the article is of the apropriate length
        # I decided at least 5 sentences!
        while len(reuters.sents(article)) < 5:
            article = random.choice(reuters.fileids())

        length = len(reuters.sents(article))//2
        summary_sentences = cfs.summarize(article, length)
        print_summary(summary_sentences)

'''
A function which generates both selections of sentences and summaries and prints them into a document.
Also creates a key.
'''
def filesForEval(cfs):

    #the number of sentences in each summary to be generated
    length = 5

    #the number of summaries to be written into the file
    number_of_summaries = 10

    #create the file containing the summaries
    summFile = open('random_order_summaries_2.txt', 'w')
    #create the file which will be the key
    keyFile = open('key_2.txt', 'w')

    #generate the appropriate number of summaries
    for n in range(number_of_summaries):
        #get a random article from the corpus
        article = random.choice(reuters.fileids())
        #make sure the article is of the apropriate length
        # I decided at least twice the length of the summary in this case.
        while len(reuters.sents(article)) < length*4:
            article = random.choice(reuters.fileids())

        #print info about the article into the summary-containing document
        summFile.write('Article #' + str(n) + '\n')
        summFile.write('\nfileid: ' + article + '\n\n')

        #print info about the article into the key document
        keyFile.write('Article #' + str(n) + '\n')
        keyFile.write('fileid: ' + article + '\n\n')

        #get a list of sentences that is the summary generated by our algorithm
        summSents = cfs.summarize(article, length)
        #insert a marker to make sure we remember it is the summary
        summSents.insert(0, 'summ')

        #get a list of sentences that were randomly ordered
        randSents = getRandom(article, length)
        #insert a marker to make sure we remember it is the random selection
        randSents.insert(0, 'rand')

        #mix up the ordering
        summs = [summSents, randSents]
        random.shuffle(summs)

        #Write the summaries into the file and write the key, in a semi-nice format
        for summ in summs:
            for i, sentence in enumerate(summ):
                if i == 0:
                    keyFile.write(sentence)
                else:
                    for word in sentence:
                        summFile.write(word + ' ')
                    summFile.write('\n')
            summFile.write('\n')
            keyFile.write(' ')
        summFile.write('\n')
        keyFile.write('\n')


    summFile.close()
    keyFile.close()

'''
A function which returns a random "imitation summary"
'''
def getRandom(article, length):
    allSents = list(enumerate(list(reuters.sents(article))))
    print(len(allSents))

    sentences = []
    sentences.append(allSents[0])
    allSents.__delitem__(0)

    for n in range(length):
        sent = random.choice(allSents)
        sentences.append(sent)
        allSents.remove(sent)

    sentences.sort()

    sentList = []
    for sent in sentences:
        sentence = sent[1]
        sentList.append(sentence)

    return sentList

'''
Print the summaries given as a 3D list ( Summaries[Sentences[Words]] )
'''
def print_summary(summary):
    for sentence in summary:
        for word in sentence:
            print(word, end=' ')
        print()
    print()

main()