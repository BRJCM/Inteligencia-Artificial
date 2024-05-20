import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Adicione esta linha

# Variáveis de entrada
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade')
velocidade_vento = ctrl.Antecedent(np.arange(0, 21, 1), 'velocidade_vento')

# Variável de saída
potencia_ar_condicionado = ctrl.Consequent(np.arange(0, 101, 1), 'potencia_ar_condicionado')

# Conjuntos fuzzy para temperatura
temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 20])
temperatura['media'] = fuzz.trimf(temperatura.universe, [10, 20, 30])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [20, 40, 40])

# Conjuntos fuzzy para umidade
umidade['baixa'] = fuzz.trimf(umidade.universe, [0, 0, 50])
umidade['media'] = fuzz.trimf(umidade.universe, [25, 50, 75])
umidade['alta'] = fuzz.trimf(umidade.universe, [50, 100, 100])

# Conjuntos fuzzy para velocidade do vento
velocidade_vento['baixa'] = fuzz.trimf(velocidade_vento.universe, [0, 0, 10])
velocidade_vento['media'] = fuzz.trimf(velocidade_vento.universe, [5, 10, 15])
velocidade_vento['alta'] = fuzz.trimf(velocidade_vento.universe, [10, 20, 20])

# Conjuntos fuzzy para potência do ar condicionado
potencia_ar_condicionado['baixa'] = fuzz.trimf(potencia_ar_condicionado.universe, [0, 0, 50])
potencia_ar_condicionado['media'] = fuzz.trimf(potencia_ar_condicionado.universe, [25, 50, 75])
potencia_ar_condicionado['alta'] = fuzz.trimf(potencia_ar_condicionado.universe, [50, 100, 100])

# Regras fuzzy
rule1 = ctrl.Rule(temperatura['baixa'] & umidade['baixa'] & velocidade_vento['baixa'], potencia_ar_condicionado['baixa'])
rule2 = ctrl.Rule(temperatura['media'] & umidade['media'] & velocidade_vento['media'], potencia_ar_condicionado['media'])
rule3 = ctrl.Rule(temperatura['alta'] & umidade['alta'] & velocidade_vento['alta'], potencia_ar_condicionado['alta'])
rule4 = ctrl.Rule(temperatura['baixa'] & umidade['alta'] & velocidade_vento['media'], potencia_ar_condicionado['media'])
rule5 = ctrl.Rule(temperatura['media'] & umidade['baixa'] & velocidade_vento['alta'], potencia_ar_condicionado['alta'])
rule6 = ctrl.Rule(temperatura['alta'] & umidade['media'] & velocidade_vento['baixa'], potencia_ar_condicionado['media'])

# Sistema de controle fuzzy
sistema_controle = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
simulador = ctrl.ControlSystemSimulation(sistema_controle)

# Entrada de valores para simulação
simulador.input['temperatura'] = 25
simulador.input['umidade'] = 60
simulador.input['velocidade_vento'] = 5

# Computar a saída
simulador.compute()

# Exibir o resultado
print(simulador.output['potencia_ar_condicionado'])

# Visualização dos conjuntos fuzzy e da saída
temperatura.view()
umidade.view()
velocidade_vento.view()
potencia_ar_condicionado.view(sim=simulador)

# Mostrar os gráficos
plt.show()
