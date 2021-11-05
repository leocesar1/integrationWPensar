from requests import get, post, put
import json 
from graphicElements.progressBar import *

# from math import *
# from datetime import *
# from time import *

class wPensarAccessPoint(object):
    def __new__(cls):
        # garanted a unique instance of a class
        if not hasattr(cls, 'instance'):
            cls.instance =super(wPensarAccessPoint, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # Global settings to access WPensar API
        # Open a private file 'accessTokenWPensar.json' and get access token to API 
        with open('accessTokenWPensar.json', 'r') as f:
            accessToken = json.loads(f)['accessToken']

        # Create a headers
        self.headers = {'Authorization': 'access_token %s' % accessToken}

    def getInformations(self, pk='All', target='alunos'):
        # This function returns a list of data or a single data, depending on the pk parameter  
        # In case of error, this function returns False
        if type(pk) == str:
            listData = []
            page = 1
            pagination = 100

            url = 'https://api.wpensar.com.br:443/%(target)s/?page=%(page)s&pagination=%(pagination)s' % {
                'page': page,
                'pagination': pagination,
                'target': target}
            try:
                nPag = ceil(loads(get(url, headers=self.headers).text)['count']/100)
                print("Realizando aquisição dos dados na plataforma WPensar...")
                printProgressBar(0, nPag, prefix='Progresso atual:',
                                suffix='Completo', length=50)
                for i in range(0, nPag):
                    page = i + 1
                    url = 'https://api.wpensar.com.br:443/%(target)s/?page=%(page)s&pagination=%(pagination)s' % {
                        'page': data['page'],
                        'pagination': data['pagination'],
                        'target': target}
                    r = get(url, headers=headers).text
                    for item in json.loads(r)['results']:
                        listData.append(item)
                    printProgressBar(i + 1, nPag, prefix='Progresso atual:',
                                    suffix='Completo', length=50)
                
                return listData
            except:
                print("Não foi possível conectar à plataforma WPensar.")
                return False

        elif type(pk) == int:
            try:
                data = {
                    'pk': pk,
                    'nome': 'teste'  # incluir dados da API
                }

                url = 'https://api.wpensar.com.br/%(target)s/%(pk)s/' % {
                    'pk': pk,
                    'target': target}
                r = json.loads(get(url, headers=self.headers).text)
                print('Operação realizada com sucesso')
                return r
            except:
                print('Ocorreu um erro ao realizar a operação. Por gentileza, repita a operação.')
                return False

        else:
            return False

# I need include this piece of code
# repeatLoop = True

# while repeatLoop:
#     option = input(
#         'Deseja realizar o backup das informações "%(target)s"? (S/N)' % {'target': target})
#     if option.upper() == 'S':
#         repeatLoop = not saveBackup(target, 'backup', listData)
#     elif option.upper() == 'N':
#         repeatLoop = False
#     else:
#         print('Opção inválida!!!')

# print('Serviço finalizado!!!')
# return True
