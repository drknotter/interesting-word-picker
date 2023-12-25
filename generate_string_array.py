#!/usr/local/bin/python3

import argparse


def main(args):
  interesting_words = []
  try:
    with open(args.interesting_words) as i:
      for interesting_word in i.readlines():
        interesting_words.append(interesting_word.rstrip())
  except:
    print("Couldn't open picked file, does it exist?")
    return

  print("<resources>")
  print("    <string-array name=\"%s\">" % (args.name))
  for word in interesting_words:
    print("        <item>%s</item>" % (word))
  print("    </string-array>")
  print("</resources>")

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate an Android string-array resource that contains interesting words')
  parser.add_argument('-i', '--interesting-words', help='The interesting words.')
  parser.add_argument('-n', '--name', help='The name of the string-array resource.')
  main(parser.parse_args())