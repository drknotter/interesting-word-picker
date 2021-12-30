#!/usr/local/bin/python3

import argparse
from datetime import datetime
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Onclick, Onmouseout, Type, Style as InlineStyle

style = """
body {
  max-width: 602px;
  min-width: 301px;
  margin: 0 auto !important;
  font-family: Tahoma, Verdana, sans-serif;
}
.month-name {
  margin: 15px 0px;
  padding: 15px;
  background-color: gray;
  font-size: 1.5rem;
}
.days {
  display: grid;
  gap: 8px 8px;
  grid-template-columns: repeat(7, 1fr)
}
.day-container {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: lightgray;
  padding: 8px;
  cursor: pointer;
}
.space {
  background-color: unset;
  cursor: unset;
}
.day {
  position: absolute;
  font-size: 1.25rem;
}
.day-container > * {
  pointer-events: none;
}
.word {
  position: absolute;
  opacity: 0;
}
"""

script = """
function dayClick(element) {
  Array.prototype.forEach.call(document.getElementsByClassName('day'), function(dayElement) { dayElement.style.opacity = '1' })
  Array.prototype.forEach.call(document.getElementsByClassName('word'), function(dayElement) { dayElement.style.opacity = '0' })
  Array.prototype.forEach.call(element.getElementsByClassName('day'), function(dayElement) { dayElement.style.opacity = '0' })
  Array.prototype.forEach.call(element.getElementsByClassName('word'), function(dayElement) { dayElement.style.opacity = '1' })
}
function dayMouseOut(element) {
  Array.prototype.forEach.call(element.getElementsByClassName('day'), function(dayElement) { dayElement.style.opacity = '1' })
  Array.prototype.forEach.call(element.getElementsByClassName('word'), function(dayElement) { dayElement.style.opacity = '0' })
}
"""

def generate_month_div(month_name, day_divs):
  return Div([Class('month-container')], 
    Div([Class('month-name')], month_name),
    Div([Class('days')], day_divs))

def generate_day_div(date, word):
  if len(word) == 0:
    return Div([Class('day-container space')])
  return Div([Class('day-container'), Onclick('dayClick(this)'), Onmouseout('dayMouseOut(this)')],
    Div([Class('day')], '%s' % (date.day)), Div([Class('word')], word))

def main(args):
  interesting_words = []
  try:
    with open(args.interesting_words) as i:
      for interesting_word in i.readlines():
        interesting_words.append(interesting_word.rstrip())
  except:
    print("Couldn't open picked file, does it exist?")
    return

  current_timestamp = datetime.strptime(args.start_date, '%m/%d/%Y').timestamp()
  current_month = ""
  divs = []
  i = 0
  while True:
    d = datetime.fromtimestamp(current_timestamp)
    m = d.strftime('%B')
    if m != current_month:
      current_month = m
      day_divs = []
      for j in range(d.weekday() + 1):
        day_divs.append(generate_day_div(d, ''))
      while True:
        day_divs.append(generate_day_div(d, interesting_words[i]))
        i += 1
        current_timestamp += 60 * 60 * 24
        d = datetime.fromtimestamp(current_timestamp)
        m = d.strftime('%B')
        if m != current_month or i >= len(interesting_words):
          break
      for j in range(d.weekday() + 1, 7):
        day_divs.append(generate_day_div(d, ''))
      divs.append(generate_month_div(current_month, day_divs))
    if i >= len(interesting_words):
      break

  html = Html([],
    Head([],
      Title([], "Word of the Day"),
      Style([], style),
      Script([Type('text/javascript')], script)
    ),
    Body([],
      divs
    )
  )
  # no closing tags are required

  # call the render() method to return tag instances as html text
  print(html.render(pretty=True))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate a site that shows interesting words')
  parser.add_argument('-i', '--interesting-words', help='The interesting words.')
  parser.add_argument('-d', '--start-date', help='The start date (mm/dd/yyyy) to show interesting words.')
  main(parser.parse_args())