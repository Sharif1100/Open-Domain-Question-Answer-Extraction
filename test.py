import wolframalpha
from nltk import word_tokenize, pos_tag, ne_chunk, conlltags2tree, tree2conlltags
import google
import wikipedia
import collections


def google_search(question):
    first_page = google.search(question, 1)

    for e in first_page:
        print(e.description)
    top_three_result = []
    i = 0
    while i < 5:
        top_three_result.append(first_page[i].description)
        i += 1
    first_search = ''.join(top_three_result).encode('ascii', 'replace')
    return first_search


def main():
    question = "When was Newton born?"
    print(google_search(question));


if __name__ == '__main__':
    main()