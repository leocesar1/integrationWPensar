import pandas as pd
from designPartners.singleton import *
from accessWPensar.accessWPensar import *

class DataBaseClickSign(metaclass = MetaSingleton):
    # get all data to include in WPensar
    def __init__(self, filename):
        if filename.split('.')[-1] == 'csv':
            self.dataframe = pd.read_csv(filename)
        elif filename.split('.')[-1] == 'xlsx' or filename.split('.')[-1] == 'xls':
            self.dataframe = pd.read_excel(filename)
        self.refreshDataFrames()

    def refreshDataFrames(self):
        self.dataframeRenovations = self.getRenovationsDataFrame()
        self.dataframeNewRegistrations = self.getNewRegistrationsDataFrame()

    def getRenovationsDataFrame(self):
        # filter by renovations case
        return self.dataframe.loc[(self.dataframe['Formulário 1 Matrícula '] == 'Renovação') & (self.dataframe['Status do documento'] == 'Finalizado')]

    def getNewRegistrationsDataFrame(self):
        # filter by new registrations case
        return self.dataframe.loc[(self.dataframe['Formulário 1 Matrícula '] == 'Renovação') & (self.dataframe['Status do documento'] == 'Finalizado')]

    def getResponsavelData(self, dataframe):
        data = []
        print(len(dataframe))
        for i in range(len(dataframe)):
            data.append({
                'nome': dataframe.loc[i,'Formulário 1 Nome'],
                'nacionalidade' : dataframe.loc[i,'Formulário 1 Nacionalidade'],
                'profissao' : dataframe.loc[i,'Formulário 1 Profissão'],
                'empregador' : dataframe.loc[i,'Formulário 1 Empregador'],
                'rg' : dataframe.loc[i,'Formulário 1 RG'],
                'cpf' : dataframe.loc[i,'Formulário 1 CPF'],
                'data_nascimento' : dataframe.loc[i,'Formulário 1 Data de Nascimento'],
                'tel_residencial' : dataframe.loc[i,'Formulário 1 Telefone Residencial'],
                'tel_cel1' : dataframe.loc[i,'Formulário 1 Telefone Celular'],
                'e-mail' : dataframe.loc[i,'Formulário 1 E-mail do signatário'],
                'cep' : dataframe.loc[i,'Formulário 1 CEP'],
                'logradouro' : dataframe.loc[i,'Formulário 1 Logradouro'],
                'bairro' : dataframe.loc[i,'Formulário 1 Bairro'],
                'cidade' : dataframe.loc[i,'Formulário 1 Cidade'],
                'estado' : dataframe.loc[i,'Formulário 1 Estado'],
            })
        return pd.DataFrame.from_records(data)

    def getResponsavelFinanceiroData(self, dataframe):
        data = []
        for i in range(len(dataframe)):
            data.append({
                'nome': dataframe.loc[i,'Formulário 1 Nome do Responsável Financeiro'],
                'nacionalidade' : dataframe.loc[i,'Formulário 1 Nacionalidade.1'],
                'profissao' : dataframe.loc[i,'Formulário 1 Profissão.1'],
                'empregador' : dataframe.loc[i,'Formulário 1 Empregador.1'],
                'rg' : dataframe.loc[i,'Formulário 1 RG.1'],
                'cpf' : dataframe.loc[i,'Formulário 1 CPF.1'],
                'data_nascimento' : dataframe.loc[i,'Formulário 1 Data de Nascimento.1'],
                'tel_residencial' : dataframe.loc[i,'Formulário 1 Telefone'],
                'tel_cel1' : dataframe.loc[i,'Formulário 1 Telefone Celular.1'],
                'e-mail' : dataframe.loc[i,'Formulário 1 E-mail do responsável financeiro'],
                'cep' : dataframe.loc[i,'Formulário 1 CEP.1'],
                'logradouro' : dataframe.loc[i,'Formulário 1 Logradouro.1'],
                'bairro' : dataframe.loc[i,'Formulário 1 Bairro.1'],
                'cidade' : dataframe.loc[i,'Formulário 1 Cidade.1'],
                'estado' : dataframe.loc[i,'Formulário 1 Estado.1'],
            })
        return pd.DataFrame.from_records(data)

    def getAlunoData(self, dataframe):
        data = []
        for i in range(len(dataframe)):
            data.append({
                'nome': dataframe.loc[i,'Formulário 1 Nome do Aluno (a)'],
                'serie' : dataframe.loc[i,'Formulário 1 Série pretendida em 2022'],
                'situacao' : dataframe.loc[i,'Formulário 1 Situação:']
            })
        return pd.DataFrame.from_records(data)