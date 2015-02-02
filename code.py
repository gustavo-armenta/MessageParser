import jsonpickle
import re
import sys
import urllib.request
from bs4 import BeautifulSoup

class MessageMetadata:
  def _parseMentions(self, raw):
    mentions = re.findall(re.escape('@') + '\w+', raw)
    for i, v in enumerate(mentions):
      mentions[i] = v[1:]
    if len(mentions) > 0:
      self.mentions = mentions
  def _parseEmoticons(self, raw):
    emoticons = re.findall('\(\w{1,15}\)', raw)
    for i, v in enumerate(emoticons):
      emoticons[i] = v[1:-1]
    if len(emoticons) > 0:
      self.emoticons = emoticons
  def _parseLinks(self, raw):
    links = []
    # regex copied from http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw)
    for url in urls:
      link = Link()
      link.url = url
      try:
        response = urllib.request.urlopen(url)
        xml = BeautifulSoup(response.read())
        link.title = xml.title.text
      except:
        print("Failed to get html.title:", sys.exc_info()[0])
      links.append(link)
    if len(links) > 0:
      self.links = links
  def parse(self, raw):
    if raw is None:
      return
    self._parseMentions(raw)
    self._parseEmoticons(raw)
    self._parseLinks(raw)

class Link:
  pass

def main(): 
  raws = [
    None,
    "",
    "@",
    "()",
    "https://invalid.url/",
    "@chris you around?",
    "Good morning! (megusta) (coffee)",
    "Olympics are starting soon; http://www.nbcolympics.com",
    "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"]

  jsonpickle.set_encoder_options('json', indent=2)

  for raw in raws:
    print(raw)
    metadata = MessageMetadata()
    metadata.parse(raw)
    print(jsonpickle.encode(metadata, unpicklable=False))
    print('====')

if __name__ == "__main__": main()