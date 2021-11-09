


# Load clicksign spreadsheet
from manipulationCSV.dataFrame import *

dataBaseClickSign = DataBaseClickSign('Relatorio.xlsx')

# Load WPensar json
from accessWPensar.dataFrame import *

dataBaseWPensar = DataBaseWPensar()

print(dataBaseWPensar.getAlunosAllInformations())