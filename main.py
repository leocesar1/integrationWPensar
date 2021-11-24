#! virtualenv/bin/env python
# from __future__ import annotations
# from abc import ABC, abstractmethod
# from typing import List
# Load clicksign spreadsheet
# from manipulationCSV.dataFrame import *

# dataBaseClickSign = DataBaseClickSign('Relatório - matrículas internas.csv')
# dataBaseClickSign = DataBaseClickSign('Relatório -matrículas internas excepcionais.csv')
# dataBaseClickSign = DataBaseClickSign('Relatório - matrículas externas.csv')
# dataBaseClickSign = DataBaseClickSign('Relatório - matrículas externas - excepcionais.csv')

# dataBaseClickSign.saveAsXls()

## Load WPensar json
# from accessWPensar.dataFrame import *

# dataBaseWPensar = DataBaseWPensar()


# # is a draft for a loop verification
# text2 = dataBaseWPensar.alunos['nome']

# for i in range(0,len(dataBaseClickSign.getAlunoData(dataBaseClickSign.dataframeRenovations))):
#     text1 = dataBaseClickSign.getAlunoData(dataBaseClickSign.dataframeRenovations).iloc[i,0]
#     for item # for index, row in self.WPensar.alunos.iterrows():
        #     if self.stringComparation(text1, row['nome']):
        #         id = row['matricula']
        #         # print(id)
        # if id is not None:
        #     return id
        # else:
        #     return Nonein text2:
#         if dataBaseWPensar.stringComparation(text1, item):
#             print(item)

from designPartners.facade import *
you = You()
you.askInclusionManager()