#!/usr/local/bin/python3

import argparse
from datetime import datetime
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Id, Onclick, Onmouseout, Type, Style as InlineStyle

style = """
html {
  font-family: Tahoma, Verdana, sans-serif;
}
.noscroll {
  overflow: hidden;
}
.calendar {
  max-width: 602px;
  min-width: 480px;
  margin: 0 auto !important;
}
#word-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: none;
  background-color: rgba(255,255,255,0.5);
  pointer-events: none;
  font-size: 1.5rem;
}
.popup-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  max-width: 75%;
  min-width: 65%;
  padding: 32px;
  background-color: gray;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
}
#date {
  text-align: start;
  flex-grow: 1;
  padding: 16px 32px;
  background-color: lightgray;
}
#word {
  text-align: center;
  padding-top: 16px;
  font-size: 3rem;
}
.month-container {
  margin: 0 16px;
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
.word {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
}
.day-container > * {
  pointer-events: none;
}
@media screen and (max-device-width: 480px) {
  .calendar {
    min-width: unset;
    max-width: unset;
    margin: 0 auto !important;
    font-family: Tahoma, Verdana, sans-serif;
  }
  #word-popup {
    font-size: 3rem;
  }
  .month-name {
    font-size: 3rem;
  }
  .day {
    font-size: 2rem;
  }
}
"""

script = """
function dayClick(element) {
  var month = element.closest('.month-container').getElementsByClassName('month-name')[0].innerHTML
  var day = element.getElementsByClassName('day')[0].innerHTML
  var word = element.getElementsByClassName('word')[0].innerHTML
  document.getElementById('date').innerHTML = `${month} ${day}`
  document.getElementById('word').innerHTML = `${word}`

  document.getElementById('word-popup').style['display'] = 'block'
  document.getElementById('word-popup').style['pointer-events'] = 'auto'
  document.getElementsByTagName('html')[0].classList.add('noscroll')
  document.getElementsByTagName('body')[0].classList.add('noscroll')
}
function wordClick() {
  document.getElementById('word-popup').style['display'] = 'none'
  document.getElementById('word-popup').style['pointer-events'] = 'none'
  document.getElementsByTagName('html')[0].classList.remove('noscroll')
  document.getElementsByTagName('body')[0].classList.remove('noscroll')
}
"""

def generate_month_div(month_name, day_divs):
  return Div([Class('month-container')], 
    Div([Class('month-name')], month_name),
    Div([Class('days')], day_divs))

def generate_day_div(date, word):
  if len(word) == 0:
    return Div([Class('day-container space')])
  return Div([Class('day-container'), Onclick('dayClick(this)')],
    [Div([Class('day')], '%s' % (date.day)), Div([Class('word')], word)])

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
      Title([], "One Square Inch"),
      Style([], style),
      Script([Type('text/javascript')], script)
    ),
    Body([],
      [
        Div([Class('calendar')], 
          divs),
        Div([Id('word-popup'), Onclick('wordClick()')],
        [
          Div([Class('popup-container')],
          [
            Div([Id('date')], ''),
            Div([Id('word')], '')
          ])
        ])
      ])
  )

  print(html.render(pretty=True))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate a site that shows interesting words')
  parser.add_argument('-i', '--interesting-words', help='The interesting words.')
  parser.add_argument('-d', '--start-date', help='The start date (mm/dd/yyyy) to show interesting words.')
  main(parser.parse_args())