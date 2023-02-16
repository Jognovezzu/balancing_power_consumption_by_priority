# Dicionário que armazena as prioridades e os valores de consumo de energia dos sistemas
dados_sistemas = {
    "id1": {"prioridade": 0,
            "consumo": 10
    },
    "id2": {"prioridade": 2,
            "consumo": 20
    },
    "id3": {"prioridade": 1,
            "consumo": 15
    },
    "id4": {"prioridade": 3,
            "consumo": 25
    },
    "id5": {"prioridade": 4,
            "consumo": 5
    }
}

# Função que retorna o valor total de consumo de energia dos sistemas com prioridade menor ou igual a uma determinada prioridade
def calcular_consumo(prioridade):
    total = 0
    for sistema, dados in dados_sistemas.items():
        if dados["prioridade"] <= prioridade:
            total += dados["consumo"]
    return total

# Loop que balanceia o consumo de energia dos sistemas
while True:
    # Recebe os dados dos sensores --->Equipe HW ------> Criar ENDPOINT para receber esses dados
    dados_sensores = receber_dados_sensores()
    
    # Atualiza os valores de consumo de energia dos sistemas com os dados recebidos dos sensores
    for sistema, valor in dados_sensores.items():
        dados_sistemas[sistema]["consumo"] = valor
    
    # Balanceia o consumo de energia dos sistemas
    for prioridade in range(5):
        consumo_atual = calcular_consumo(prioridade)
        consumo_maximo = prioridade * 50  # Define o consumo máximo permitido para cada prioridade
        if consumo_atual > consumo_maximo:
            # Reduz o consumo de energia dos sistemas com prioridade menor ou igual a prioridade atual
            for sistema, dados in dados_sistemas.items():
                if dados["prioridade"] <= prioridade:
                    novo_valor = dados["consumo"] - ((consumo_atual - consumo_maximo) / (dados["prioridade"] + 1))
                    if novo_valor < 0:
                        novo_valor = 0
                    dados_sistemas[sistema]["consumo"] = novo_valor