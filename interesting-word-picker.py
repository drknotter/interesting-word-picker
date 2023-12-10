#!/usr/local/bin/python3

import argparse
import functools
import json
import random
import readchar

def main(args):
  picked_words = set()
  try:
    with open(args.picked) as picked_file:
      for picked_word in picked_file.readlines():
        picked_words.add(picked_word.rstrip())
    print("Read %d picked words." % (len(picked_words)))
  except:
    print("Couldn't open picked file, does it exist?")

  with open('./WebstersEnglishDictionary/dictionary_compact.json') as d:
    dictionary = json.load(d)
    words_and_weights = list(map(lambda item: (item[0], len(item[1]) ** 2), dictionary.items()))
    original_length = len(words_and_weights)
    words_and_weights = list(filter(lambda item: item[0] not in picked_words, words_and_weights))
    print("Read %d words from dictionary, removed %d." % (original_length, original_length - len(words_and_weights)))
    words_and_weights = sorted(words_and_weights, key=lambda i: i[1], reverse=True)

  picked_count = 0
  with open(args.picked, 'a') as picked_file:
    while True:
      total_weight = sum(list(map(lambda item: item[1], words_and_weights)))
      t = random.randrange(total_weight)
      s = 0
      i = 0
      while s < t:
        s += words_and_weights[i][1]
        i += 1
      word = words_and_weights[i][0]
      del words_and_weights[i]
      print('Pick %s? (y/n/c) (picked %d so far)' % (word, picked_count))
      choice = readchar.readchar()
      if choice == 'y':
        picked_count += 1
        picked_file.write('%s\n' % (word))
      if choice == 'c':
        break

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Pick interesting words at random and save them to a file.')
  parser.add_argument('-p', '--picked', help='The words that have already been picked.')
  main(parser.parse_args())