import requests
from dataclasses import dataclass
from os import environ
import string
import json
import hashlib


@dataclass
class Response():
    numero_casas: int
    token: str
    cifrado: str
    decifrado: str
    resumo_criptografico: str


class Challenge:
    def __init__(self):
        self.endpoint = f"https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={environ.get('CODENATION_TOKEN')}"
        self.post_endpoint = f"https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={environ.get('CODENATION_TOKEN')}"
        self.alphabet = tuple(string.ascii_lowercase)
        self.alphabet_dict = {val: idx for idx,
                              val in enumerate(self.alphabet)}
        self.response = Response(
            **json.loads(requests.get(self.endpoint).text))

    def process(self):
        self.decode()
        self.create_hash()
        self.save_json()
        self.submit()

    def decode(self):
        to_decode = self.response.cifrado.split(' ')
        _decoded = []
        _weirdos = {}
        for x in to_decode:
            try:
                _decoded.append(''.join([self.alphabet[i-self.response.numero_casas]
                                         for i in [self.alphabet_dict[i] for i in x]]))
            except KeyError:
                comma_case = x.split(',')
                dot_case = x.split('.')
                if len(comma_case) == 2:
                    x = comma_case
                    ab = []
                    for a in x:
                        ab.append(''.join([self.alphabet[i-self.response.numero_casas]
                                           for i in [self.alphabet_dict[i] for i in a]]))
                    _decoded.append(','.join(ab))
                elif len(dot_case) == 2:
                    x = dot_case
                    ab = []
                    for a in x:
                        ab.append(''.join([self.alphabet[i-self.response.numero_casas]
                                           for i in [self.alphabet_dict[i] for i in a]]))
                    _decoded.append('.'.join(ab))

            self.response.decifrado = ' '.join(_decoded)

    def create_hash(self):
        self.response.resumo_criptografico = hashlib.sha1(
            bytes(self.response.decifrado, 'utf-8')).hexdigest()

    def save_json(self):
        with open("./answer.json", "w") as fp:
            json.dump(self.response.__dict__, fp)

    def submit(self):
        files = {'answer': open('./answer.json', 'rb'),
                 'Content-type': 'multipart/form-data',
                 'Content-Type': 'application/json'}
        r = requests.post(self.post_endpoint, files=files)
        print(r.text, r.status_code)


if __name__ == "__main__":
    Challenge().process()
