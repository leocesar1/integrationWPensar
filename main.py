


# Load clicksign spreadsheet
from manipulationCSV.dataFrame import *

dataBaseClickSign = DataBaseClickSign('Relatorio.xlsx')

# Load WPensar json
from accessWPensar.dataFrame import *

dataBaseWPensar = DataBaseWPensar()

dataBaseWPensar.getAlunosAllInformations()

print(dataBaseWPensar.alunos)
print(dataBaseWPensar.responsaveis)
print(dataBaseWPensar.alunosResponsaveis)