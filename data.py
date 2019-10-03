'''

from datetime import datetime
from datetime import timedelta

data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")

#print(data_e_hora_em_texto.split())
ultimo = timedelta(days=0, hours=int(ultimo[0]), minutes=int(ultimo[1]), seconds=int(ultimo[2]))

novo = timedelta(days=0, hours=int(novo[0]), minutes=int(novo[1]), seconds=int(novo[2]))

result = novo - ultimo

if result.total_seconds() > 30:  # ajustar
   print("Alarme")


'''

