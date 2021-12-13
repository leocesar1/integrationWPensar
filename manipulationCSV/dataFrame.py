from math import nan, isnan
from numpy import NaN
import pandas as pd
from designPartners.singleton import *
from accessWPensar.accessWPensar import *

class DataBaseClickSign(metaclass = MetaSingleton):
    # get all data to include in WPensar
    def __init__(self, filename):
        import os     
        filename = os.path.join(os.path.dirname('__file__'), 'planilha_clicksign', filename)

        try:
            if filename.split('.')[-1] == 'csv':
                self.dataframeOriginal = pd.read_csv(filename)
            elif filename.split('.')[-1] == 'xlsx' or filename.split('.')[-1] == 'xls':
                self.dataframeOriginal = pd.read_excel(filename)
        except:
            print('Não foi possível carregar a planilha indicada. Verifique os dados e tente novamente.')
            self.dataframeTreated = None
            # self.dataframeRenovations = pd.DataFrame({'A' : []})
            # self.dataframeNewRegistrations = pd.DataFrame({'A' : []})
        else:
            self.treatDataFrame()
        
    def treatDataFrame(self):
        self.getDocumentsInformations()
        self.getAlunoData()
        self.getResponsavelOneData()
        self.getResponsavelTwoData()
        self.getResponsavelFinanceiroData()
        self.setInclusionsSituations()
        # self.applyFilters()
        self.getReport()

    def isNewStudent(self, studentSituation):
        listOfPossibilitiesNewStudents = (
            'Aluno Novo (dependente de associado ativo)',
            'Novo aluno (ingresso externo) ',
            'Novo aluno (dependente de ex - aluno da escola)',
            ' Novo aluno (dependente de associado inativo)',
            'Ex - aluno (dependente de associado inativo)',
            nan
        )

        listOfPossibilitiesOldStudents = ('Aluno da Escola')
        try:
            if studentSituation in listOfPossibilitiesNewStudents:
                print(True)
                return True
            elif isnan(studentSituation):
                print(True)
                return True
            elif studentSituation in listOfPossibilitiesOldStudents:
                print(True)
                return False
            else:
                print(None)
                return None
        except:
            return None

    def isNewResponsible(self, responsibleSituation):
        # filter by renovations case
        

        listOfPossibilitiesOldResponsibles = (   
        )

        listOfPossibilitiesNewResponsibles = (
            'Novo aluno (ingresso externo) ',
            'Ex - aluno (dependente de associado inativo)',
            'Novo aluno (dependente de ex - aluno da escola)',
            'Aluno da Escola',
            'Aluno Novo (dependente de associado ativo)',
            ' Novo aluno (dependente de associado inativo)'
        )

        if responsibleSituation in listOfPossibilitiesNewResponsibles:
            return True
        elif responsibleSituation in listOfPossibilitiesOldResponsibles:
            return False
        else:
            return None
        
    def isEmpty(self, text):
        # verify if a field is a empty field
        return True if not text else False

    def isFinished(self, text):
        # verify if a field is a empty field
        return True if "Finalizado" else False

    def isTestStudent(self, text):
        # verify if is a teste
        # students name
        # return True if isn't a test
        listTestNames = [
            'Jéssica Nascimento Lacerda Domingos',
            'Teste ',
            'Testando ',
            'aaaaaaaaaaaaaaa',
            'Minga',
            'Ele',
            'minga ',
            'Caetano Domingos Lacerda',
            'Gabi',
            'Caetano Domingos',
            'Amanda',
            'Gabriella Veloni',
            'Kyra Leles Amantea'
        ]
        return True if text in listTestNames else False

    def setInclusionsSituations(self):
        # includes all        
        self.dataframeTreated['novo_aluno'] = self.dataframeTreated.apply(lambda x: self.isNewStudent(x['situacao']), axis = 1)
        self.dataframeTreated['novo_responsavel'] = self.dataframeTreated.apply(lambda x: self.isNewResponsible(x['situacao']), axis = 1)
        self.dataframeTreated['teste'] = self.dataframeTreated.apply(lambda x: self.isTestStudent(x['nomeAluno']), axis = 1)
        self.dataframeTreated['finalizado'] = self.dataframeTreated.apply(lambda x: self.isFinished(x['status']), axis = 1)

    def getDocumentsInformations(self, dataframe = None):
        dataframe = self.dataframeOriginal if dataframe is None else dataframe
        
        self.dataframeTreated = dataframe[['Status do documento']].copy()
        self.dataframeTreated = self.dataframeTreated.rename(columns= {'Status do documento': 'status'})
        # return self.dataframeTreated

    def getAlunoData(self, dataframe = None):
        dataframe = self.dataframeOriginal if dataframe is None else dataframe
        
        try:
            self.dataframeTreated['nomeAluno'] = dataframe['Formulário 1 Nome do Aluno (a)']
        except:
            self.dataframeTreated['nomeAluno'] = dataframe['Formulário 1 Nome completo do Aluno (a) :']
        finally:
            try:
                self.dataframeTreated['serie2022'] = dataframe['Formulário 1 Série pretendida em 2022']
            except:
                self.dataframeTreated['serie2022'] = dataframe['Formulário 1 Série pretendida em 2022:']
            finally:
                try:
                    self.dataframeTreated['situacao'] = dataframe['Formulário 1 Situação:']
                except:
                    try:
                        self.dataframeTreated['situacao'] = dataframe['Formulário 1 Situação do Aluno:']
                    except:
                        self.dataframeTreated['situacao'] = dataframe['Formulário 1 Matrícula']
        return self.dataframeTreated

    def getResponsavelFinanceiroData(self, dataframe = None, target = 'resp_finc', radical ='Formulário'):
        dataframe = self.dataframeOriginal if dataframe is None else dataframe
        
        try:
            self.dataframeTreated['resp_finc_nome'] = dataframe['Formulário 1 Nome do Responsável Financeiro']
        except:
            try:
                self.dataframeTreated['resp_finc_nome'] = dataframe['Formulário 1 Responsável Financeiro - Caso seja diferente do Primeiro Associado assinalar "outro", informar o nome completo no campo ao lado e anexar os documentos na seção "Documentos - Responsável Financeiro"']
            except:
                self.dataframeTreated['resp_finc_nome'] = dataframe['Formulário 1 Responsável Financeiro - Caso seja diferente do Primeiro e Segundo Associado assinalar "outro", informar o nome completo no campo ao lado e anexar os documentos na seção "Documentos - Responsável Financeiro"']
        finally:
            try:
                self.dataframeTreated['resp_finc_nacionalidade'] = dataframe['Formulário 1 Nacionalidade do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_nacionalidade'] = dataframe['Formulário 1 Nacionalidade.1']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_profissao'] = dataframe['Formulário 1 Profissão do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_profissao'] = dataframe['Formulário 1 Profissão.1']
                except:
                    pass
            
            try:
                self.dataframeTreated['resp_finc_empregador'] = dataframe['Formulário 1 Empregador do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_empregador'] = dataframe['Formulário 1 Empregador.1']
                except:
                    pass
                
            try:
                self.dataframeTreated['resp_finc_rg'] = dataframe['Formulário 1 RG do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_rg'] = dataframe['Formulário 1 RG.1']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_cpf'] = dataframe['Formulário 1 CPF do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_cpf'] = dataframe['Formulário 1 CPF.1']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento do Responsável Financeiro'].apply(lambda x: x.replace(' ','').replace('/','-'))
            except:
                try:
                    self.dataframeTreated['resp_finc_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento.1'].apply(lambda x: x.replace(' ','').replace('/','-'))
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_tel_residencial'] = dataframe['Formulário 1 Telefone Residencial do Responsável Financeiro ']
            except:
                try:
                    self.dataframeTreated['resp_finc_tel_residencial'] = dataframe['Formulário 1 Telefone']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_tel_celular'] = dataframe['Formulário 1 Telefone Celular do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_tel_celular'] = dataframe['Formulário 1 Telefone - Responsável Financeiro']
                except:
                    self.dataframeTreated['resp_finc_tel_celular'] = dataframe['Formulário 1 Telefone Celular.1']
            try:
                self.dataframeTreated['resp_finc_email'] = dataframe['Formulário 1 E-mail do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_email'] = dataframe['Formulário 1 E-mail - Responsável Financeiro']
                except:
                    try:
                        self.dataframeTreated['resp_finc_email'] = dataframe['Formulário 1 E-mail do responsável financeiro']
                    except:
                        pass
            try:
                self.dataframeTreated['resp_finc_cep'] = dataframe['Formulário 1 CEP do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_cep'] = dataframe['Formulário 1 CEP - Responsável Financeiro']
                except:
                    try:
                        self.dataframeTreated['resp_finc_cep'] = dataframe['Formulário 1 CEP.1']
                    except:
                        pass
            try:
                self.dataframeTreated['resp_finc_logradouro'] = dataframe['Formulário 1 Logradouro do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_logradouro'] = dataframe['Formulário 1 Logradouro.1']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_bairro'] = dataframe['Formulário 1 Bairro do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_bairro'] = dataframe['Formulário 1 Bairro.1']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_cidade'] = dataframe['Formulário 1 Cidade do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_cidade'] = dataframe['Formulário 1 Cidade.1']
                except:
                    pass
            try:
                self.dataframeTreated['resp_finc_estado'] = dataframe['Formulário 1 Estado do Responsável Financeiro']
            except:
                try:
                    self.dataframeTreated['resp_finc_estado'] = dataframe['Formulário 1 Estado.1']
                except:
                    pass
                                                                   
    def getResponsavelTwoData(self, dataframe = None):
        dataframe = self.dataframeOriginal if dataframe is None else dataframe
        
        try:
            self.dataframeTreated['resp2_nome'] = dataframe['Formulário 1 Segundo Associado']
        except:
            try:
                self.dataframeTreated['resp2_nome'] = dataframe['Formulário 1 Nome - Segundo Associado']
            except:
                pass
        finally:
            try:
                self.dataframeTreated['resp2_nacionalidade'] = dataframe['Formulário 1 Nacionalidade do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_nacionalidade'] = dataframe['Formulário 1 Nacionalidade - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_profissao'] = dataframe['Formulário 1 Profissão do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_profissao'] = dataframe['Formulário 1 Profissão - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_empregador'] = dataframe['Formulário 1 Empregador do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_empregador'] = dataframe['Formulário 1 Empregador - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_rg'] = dataframe['Formulário 1 RG do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_rg'] = dataframe['Formulário 1 RG - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_cpf'] = dataframe['Formulário 1 CPF do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_cpf'] = dataframe['Formulário 1 CPF - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento do Segundo Associado'].apply(lambda x: x.replace(' ','').replace('/','-'))
            except:
                try:
                    self.dataframeTreated['resp2_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento - Segundo Associado'].apply(lambda x: x.replace(' ','').replace('/','-'))
                except:
                    pass
            try:
                self.dataframeTreated['resp2_tel_residencial'] = dataframe['Formulário 1 Telefone Residencial do Segundo Associado'].apply(lambda x: x.replace(' ','').replace('/','-'))
            except:
                try:
                    self.dataframeTreated['resp2_tel_residencial'] = dataframe['Formulário 1 Telefone - Segundo Associado']
                except:
                    try:
                        self.dataframeTreated['resp2_tel_residencial'] = dataframe['Formulário 1 Telefone Residencial - Segundo Associado']
                    except:
                        pass
            try:
                self.dataframeTreated['resp2_tel_celular'] = dataframe['Formulário 1 Telefone Celular do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_tel_celular'] = dataframe['Formulário 1 Celular - Segundo Associado']
                except:
                    try:
                        self.dataframeTreated['resp2_tel_celular'] = dataframe['Formulário 1 Telefone Celular - Segundo Associado']
                    except:
                        pass
            try:
                self.dataframeTreated['resp2_email'] = dataframe['Formulário 1 E-mail do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_email'] = dataframe['Formulário 1 E-mail - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_cep'] = dataframe['Formulário 1 CEP do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_cep'] = dataframe['Formulário 1 CEP - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_logradouro'] = dataframe['Formulário 1 Logradouro do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_logradouro'] = dataframe['Formulário 1 Logradouro - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_numero'] = dataframe['Formulário 1 Número do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_numero'] = dataframe['Formulário 1 Número - Segundo Associado']
                except:
                    try:
                        self.dataframeTreated['resp2_numero'] = dataframe['Formulário 1 Número -  Segundo Associado']
                    except:
                        pass
            try:
                self.dataframeTreated['resp2_bairro'] = dataframe['Formulário 1 Bairro do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_bairro'] = dataframe['Formulário 1 Bairro - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_complemento'] = dataframe['Formulário 1 Complemento do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_complemento'] = dataframe['Formulário 1 Complemento - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_cidade'] = dataframe['Formulário 1 Cidade do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_cidade'] = dataframe['Formulário 1 Cidade - Segundo Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp2_estado'] = dataframe['Formulário 1 Estado do Segundo Associado']
            except:
                try:
                    self.dataframeTreated['resp2_estado'] = dataframe['Formulário 1 Estado - Segundo Associado']
                except:
                    pass
            
    def getResponsavelOneData(self, dataframe = None):
        dataframe = self.dataframeOriginal if dataframe is None else dataframe
        
        try:
            self.dataframeTreated['resp1_nome'] = dataframe['Formulário 1 Nome']
        except:
            self.dataframeTreated['resp1_nome'] = dataframe['Formulário 1 Primeiro Associado']
        finally:
            try:
                self.dataframeTreated['resp1_nacionalidade'] = dataframe['Formulário 1 Nacionalidade do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_nacionalidade'] = dataframe['Formulário 1 Nacionalidade - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_nacionalidade'] = dataframe['Formulário 1 Nacionalidade']
            try:
                self.dataframeTreated['resp1_profissao'] = dataframe['Formulário 1 Profissão do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_profissao'] = dataframe['Formulário 1 Profissão - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_profissao'] = dataframe['Formulário 1 Profissão']
            try:
                self.dataframeTreated['resp1_empregador'] = dataframe['Formulário 1 Empregador do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_empregador'] = dataframe['Formulário 1 Empregador - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_empregador'] = dataframe['Formulário 1 Empregador']
            try:
                self.dataframeTreated['resp1_rg'] = dataframe['Formulário 1 RG do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_rg'] = dataframe['Formulário 1 RG - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_rg'] = dataframe['Formulário 1 RG']
            try:
                self.dataframeTreated['resp1_cpf'] = dataframe['Formulário 1 CPF do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_cpf'] = dataframe['Formulário 1 CPF - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_cpf'] = dataframe['Formulário 1 CPF']
            try:
                self.dataframeTreated['resp1_cpf'] = dataframe['Formulário 1 CPF do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_cpf'] = dataframe['Formulário 1 CPF - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_cpf'] = dataframe['Formulário 1 CPF']
            try:
                self.dataframeTreated['resp1_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento do Primeiro Associado'].apply(lambda x: x.replace(' ','').replace('/','-'))
            except:
                try:
                    self.dataframeTreated['resp1_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento - Primeiro Associado'].apply(lambda x: x.replace(' ','').replace('/','-'))
                except:
                    try:
                        self.dataframeTreated['resp1_dt_nascimento'] = dataframe['Formulário 1 Data de Nascimento'].apply(lambda x: x.replace(' ','').replace('/','-'))
                    except:
                        pass
            try:
                self.dataframeTreated['resp1_tel_residencial'] = dataframe['Formulário 1 Telefone Residencial do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_tel_residencial'] = dataframe['Formulário 1 Telefone - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_tel_residencial'] = dataframe['Formulário 1 Telefone Residencial']
            try:
                self.dataframeTreated['resp1_tel_celular'] = dataframe['Formulário 1 Telefone Celular do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_tel_celular'] = dataframe['Formulário 1 Celular - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_tel_celular'] = dataframe['Formulário 1 Telefone Celular']
            try:
                self.dataframeTreated['resp1_email'] = dataframe['Formulário 1 E-mail do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_email'] = dataframe['Formulário 1 E-mail - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_email'] = dataframe['Formulário 1 E-mail do signatário']
            try:
                self.dataframeTreated['resp1_cep'] = dataframe['Formulário 1 CEP do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_cep'] = dataframe['Formulário 1 CEP - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_cep'] = dataframe['Formulário 1 CEP']
            try:
                self.dataframeTreated['resp1_logradouro'] = dataframe['Formulário 1 Logradouro do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_logradouro'] = dataframe['Formulário 1 Logradouro - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_logradouro'] = dataframe['Formulário 1 Logradouro']
            try:
                self.dataframeTreated['resp1_numero'] = dataframe['Formulário 1 Número do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_numero'] = dataframe['Formulário 1 Número - Primeiro Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp1_bairro'] = dataframe['Formulário 1 Bairro do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_bairro'] = dataframe['Formulário 1 Bairro - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_bairro'] = dataframe['Formulário 1 Bairro']
            try:
                self.dataframeTreated['resp1_complemento'] = dataframe['Formulário 1 Complemento do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_complemento'] = dataframe['Formulário 1 Complemento - Primeiro Associado']
                except:
                    pass
            try:
                self.dataframeTreated['resp1_cidade'] = dataframe['Formulário 1 Cidade do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_cidade'] = dataframe['Formulário 1 Cidade - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_cidade'] = dataframe['Formulário 1 Cidade']
            try:
                self.dataframeTreated['resp1_estado'] = dataframe['Formulário 1 Estado do Primeiro Associado']
            except:
                try:
                    self.dataframeTreated['resp1_estado'] = dataframe['Formulário 1 Estado - Primeiro Associado']
                except:
                    self.dataframeTreated['resp1_estado'] = dataframe['Formulário 1 Estado']
            
    def getRenovation(self, dataframe = None):
        # filter by renovations case
        dataframe = self.dataframeTreated if dataframe is None else dataframe
        
        return self.dataframe.loc[((self.dataframe['situacao'] == 'Aluno novo') or (self.dataframe['situacao'] == '')) & (self.dataframe['Status do documento'] == 'Finalizado')]

    def saveAsXls(self, dataframe = None):
        dataframe = self.dataframeTreated if dataframe is None else dataframe
        
        import os
        import xlwt     
        filename = os.path.join(os.path.dirname('__file__'), 'reports_folder', 'exportTestFile.xls')
        dataframe.to_excel(filename)

    def getReport(self):
        # All data
        totalData = len(self.dataframeTreated)
        columnNames = self.dataframeTreated.columns
        finishedData = self.dataframeTreated.query('status == "Finalizado"')
        f"""
        Foram importados {totalData} dado(s). Desse total, {len(finishedData)} foram finalizados.
        """
       
        print('Avaliação das inclusões...')
        print('--------------------------------------------------------')
        print(f'Foram importados {totalData} dados.')
        
        print(f'Documentos finalizados: {len(finishedData)}')
        
        # New students
        print('--------------------------------------------------------')
        newData = self.dataframeTreated.query('status == "Finalizado" & (novo_aluno == True) ')
        print(f'Novos alunos: {len(newData)} dados')
        
        # New Responsables
        print('--------------------------------------------------------')
        newData = self.dataframeTreated.query('status == "Finalizado" & (novo_responsavel == True) ')
        print(f'Novos responsáveis: {len(newData)} dados')

        # Old students
        print('--------------------------------------------------------')
        newData = self.dataframeTreated.query('status == "Finalizado" & (novo_aluno == False) ')
        print(f'Alunos para renovação ou retorno de ex-alunos: {len(newData)} dados')
        
        # Old Responsibles
        print('--------------------------------------------------------')
        newData = self.dataframeTreated.query('status == "Finalizado" & (novo_responsavel == False) ')
        print(f'Responsáveis já incluídos no sistema: {len(newData)} dados')


        # Test data
        print('--------------------------------------------------------')
        newData = self.dataframeTreated.query('status == "Finalizado" & (teste == True) ')
        print(f'Dados com alunos teste e finalizados: {len(newData)} dados' )
        
    