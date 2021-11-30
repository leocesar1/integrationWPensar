from requests import get, post, put
import json 
from graphicElements.progressBar import *
from designPartners.singleton import *

from math import ceil
import datetime
# from time import *

class dataMatricula(object):
    """
    This class creates a partner to include students data
    """
    def __init__(self, data):
        self.mataluno = data['matriculaWPensar']
        self.codTurma = self.getTurma(data['serie2022'])

    def getTurma(self, turma):
        turma = turma.replace('Berçário II - Integral', "Berçário II (Integral)")
        turma = turma.replace('Berçário II - Parcial', "Berçário II (Parcial)")
        turma = turma.replace('Maternal I - Integral', "Maternal I (Integral)")
        turma = turma.replace('Maternal I - Tarde', "Maternal I (Parcial)")
        turma = turma.replace('Maternal I - Manhã', "Maternal I (Parcial)")
        turma = turma.replace('Maternal II - Integral', "Maternal I (Integral)")
        turma = turma.replace('Maternal II - Manhã', "Maternal II (Parcial)")
        turma = turma.replace('Maternal II - Tarde', "Maternal II (Parcial)")

        turma = turma.replace('Pré- Escola I - Manhã', "Pré I (Parcial)")
        turma = turma.replace('Pré- Escola I - Tarde', "Pré I (Parcial)")
        turma = turma.replace('Pré- Escola I - Integral', "Pré I (Integral)")
        turma = turma.replace('Pré- Escola II - Manhã', "Pré II (Parcial)")
        turma = turma.replace('Pré- Escola II - Tarde', "Pré II (Parcial)")
        turma = turma.replace('Pré- Escola II - Integral', "Pré II (Integral)")

        turma = turma.replace('º', "")
        turma = turma.replace('EF I - Manhã', "EFI")
        turma = turma.replace('EF I - Tarde', "EFI")
        turma = turma.replace('EF II - Manhã', "EFII")
        turma = turma.replace('EF II - Tarde', "EFII")
        
        turma = turma.replace('Ensino Médio - Manhã', 'EM')
        turma = turma.replace('Ensino Médio - Tarde', 'EM')

        listTurmas = {
            "Berçário II (Parcial)": 756,
            "Berçário II (Integral)": 756,
            "Maternal I (Parcial)": 733,
            "Maternal I (Integral)": 733,
            "Maternal II (Parcial)": 738,
            "Maternal II (Integral)": 738,
            "Pré I (Parcial)": 740,
            "Pré I (Integral)": 740,
            "Pré II (Parcial)": 739,
            "Pré II (Integral)": 739,
            "1 ano - EFI": 741,
            "2 ano - EFI": 742,
            "3 ano - EFI": 743,
            "4 ano - EFI": 744,
            "5 ano - EFI": 745,
            "6 ano - EFII": 746,
            "7 ano - EFII": 747,
            "8 ano - EFII": 748,
            "9 ano - EFII": 757,
            "1 ano - EM": 749,
            "2 ano - EM": 750,
            "3 ano - EM": 751
        }

        return listTurmas[turma]


    def toJson(self):
        response = {
            'mataluno': self.mataluno,
            'codturma': self.codTurma,
            }

        return response

class dataAlunoResponsavel(object):
    """
    This class creates a partner to include students data
    """
    def __init__(self, data):
        self.pk = data['codigoAlunoResponsavel'] if data['codigoAlunoResponsavel'] != 0 else False 
        self.mataluno = data['matriculaWPensar']
        self.codresponsavel =data['codigoResponsavel']

    def toJson(self):
        response = {
            'mataluno': self.mataluno,
            'codresponsavel': self.codresponsavel
            }
        if self.pk is not False:
            response['pk'] = self.pk
        return response

class dataResponsavel(object):
    """
    This class creates a partner to include responsible data
    """
    def __init__(self, data):
        self.codigo = data['codigoResponsavel'] if data['codigoResponsavel'] != 0 else "" 
        self.nome = data['nomeResponsavel'] if data['nomeResponsavel'] != "" else ""
        self.email = data['emailResponsavel'] if data['emailResponsavel'] != "" else ""
        self.cpf = data['cpfResponsavel'] if data['cpfResponsavel'] != "" else ""
        self.celular = data['celularResponsavel'] if data['celularResponsavel'] != "" else ""
        # self.sexo = data['sexoResponsavel if = data['se != "" else ""']
        self.datanascimento = datetime.datetime.strptime(data['dataNascimentoResponsavel'], "%d-%m-%Y").strftime("%Y-%m-%d") if data['dataNascimentoResponsavel'] != "" else ""
        # self.estadocivil = data['estadoCivilResponsavel if = data['es != "" else ""']
        self.nacionalidade = data['nacionalidadeResponsavel'] if data['nacionalidadeResponsavel'] != "" else ""
        self.profissao = data['profissaoResponsavel'] if data['profissaoResponsavel'] != "" else ""
        self.identidade = data['identidadeResponsavel'] if data['identidadeResponsavel'] != "" else ""
        self.telefone = data['telefoneResponsavel'] if data['telefoneResponsavel'] != "" else ""
        self.cep = data['cepResponsavel'] if data['cepResponsavel'] != "" else ""
        self.logradouro = data['logradouroResponsavel'] if data['logradouroResponsavel'] != "" else ""
        self.numlogradouro = data['numlogradouroResponsavel'] if data['numlogradouroResponsavel'] != "" else ""
        self.complemento = data['complementoResponsavel'] if data['complementoResponsavel'] != "" else ""
        
    def toJson(self):
        response = {
            'nome': self.nome
            }
        if self.codigo is not False:
            response['codigo'] = self.codigo 
        
        response['email'] = self.email
        response['cpf'] = self.cpf
        response['celular'] = self.celular
        # response['sexo'] = self.sexo
        response['datanascimento'] = self.datanascimento
        # response['estadocivil'] = self.estadocivil
        response['nacionalidade'] = self.nacionalidade
        response['profissao'] = self.profissao
        response['identidade'] = self.identidade
        response['telefone'] = self.telefone
        response['cep'] = self.cep
        response['logradouro'] = self.logradouro
        response['numlogradouro'] = self.numlogradouro
        response['complemento'] = self.complemento
        # response['escolaridadeformacao'] = self.escolaridadeformacao

        response = {k: v for k, v in response.items() if v != '' and v != None}
        
        return response

class dataAluno(object):
    """
    This class creates a partner to include students data
    """
    def __init__(self, data):
        self.matricula = data['matriculaWPensar'] if data['matriculaWPensar'] != 0 else False 
        self.nome = data['nomeAluno']

    def toJson(self):
        response = {
            'nome': self.nome
            }
        if self.matricula is not False:
            response['matricula'] = self.matricula
        return response

class wPensarAccessPoint(metaclass = MetaSingleton):
    def __init__(self):
        # Global settings to access WPensar API
        # Open a private file 'accessTokenWPensar.json' and get access token to API
        
        # Access the file with credentials
        import os
        print('Acessando credenciais da WPensar')
        try:
            fileTokenName = os.path.join(os.path.dirname(__file__),'accessTokenWPensar.json')
            print('Chave carregada')
        except:
            print('Credenciais inválidas.')
            fileTokenName = False

        if fileTokenName: 
            with open(fileTokenName, 'r', encoding= 'utf-8') as f:
                accessToken = accessToken = json.loads(f.read())['accessToken']

            # Create a headers
            self.headers = {'Authorization': 'access_token %s' % accessToken}

            # Testing token
            try:
                print('Testando acesso à plataforma WPensar')
                self.getInformations(pk = 1)
                print('Acesso permitido')
            except:
                print('Erro ao acessar a plataforma WPensar')
        else:
            print('Não foi possível carregar a credencial')

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
                nPag = ceil(json.loads(get(url, headers=self.headers).text)['count']/100)
                print("Realizando aquisição dos dados na plataforma WPensar...")
                printProgressBar(0, nPag, prefix='Progresso atual:',
                                suffix='Completo', length=50)
                for i in range(0, nPag):
                    page = i + 1
                    url = 'https://api.wpensar.com.br:443/%(target)s/?page=%(page)s&pagination=%(pagination)s' % {
                        'page': page,
                        'pagination': pagination,
                        'target': target}
                    r = get(url, headers=self.headers).text
                    for item in json.loads(r, encoding='utf-8')['results']:
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
                r = json.loads(get(url, headers=self.headers).text, encoding='utf-8')
                print('Operação realizada com sucesso')
                return [r]
            except:
                print('Ocorreu um erro ao realizar a operação. Por gentileza, repita a operação.')
                return False

        else:
            return False

    def updateData(self, pk = 'New', target = 'alunos', dataJson = None):
        url = f'https://api.wpensar.com.br/{target}/' if type(pk) == str else f'https://api.wpensar.com.br/{target}/{pk}/' 
        
        try:
            if type(pk) == str:        
                r = post(url, headers=self.headers, data = dataJson).json()
            else:
                r = put(url, headers=self.headers, data = dataJson).json()

            return r
        except:
            print("Não foi possível inserir os dados na plataforma WPensar.")
            return False
