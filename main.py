import requests
from dataclasses import dataclass
from os import environ
import string
import json

@dataclass
class Challenge:
  endpoint: f"https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={environ.get('CODENATION_TOKEN')}"
  alphabet: tuple(string.ascii_lowercase)
  
  def endpoint_response(self) -> json:
    return requests.get(self.endpoint).text

c = Challenge()

with open("./answer.json", "w") as fp:
    json.dump(c.endpoint_response, fp)