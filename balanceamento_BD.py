from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float
import time

# Conexão com o banco de dados

PRIORITY_PATH = 'sqlite:///energy_data.db'
engine = create_engine(PRIORITY_PATH)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

# Definição da classe para a tabela de energia
class EnergySystem(Base):
    __tablename__ = 'energy_system'
    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    priority = Column(Integer)
    consumption = Column(Float)

# Definição do limite máximo de consumo por prioridade
max_consumption_by_priority = {
    0: 100,
    1: 75,
    2: 50,
    3: 25,
    4: 10
}

# Loop infinito para leitura dos dados de consumo em tempo real -----> Alterar para parar com a execucao do Sistema
while True:
    # Leitura dos dados de consumo dos sensores ----> Alterar para ENDPOINT
    # name (INT): consumption
    sensor_data = {
        1: 50.2,
        2: 20.5,
        3: 35.1,
        4: 17.3,
        5: 12.6
    }
    
    # Leitura dos dados do banco de dados
    energy_data = session.query(EnergySystem).all()

    # Atualização do consumo dos sistemas no banco de dados
    for system in energy_data:
        system.consumption = sensor_data[system.id]
        session.commit()

    # Balanceamento de energia por prioridades
    for priority in range(5):
        systems_with_priority = [s for s in energy_data if s.priority == priority]
        total_consumption = sum(s.consumption for s in systems_with_priority)


        if total_consumption > max_consumption_by_priority[priority]:
            for i in range(priority, 5):
                systems_with_priority = [s for s in energy_data if s.priority == i]
                total_consumption = sum(s.consumption for s in systems_with_priority)
                if total_consumption < max_consumption_by_priority[i]:
                    remaining_consumption = max_consumption_by_priority[i] - total_consumption
                    for system in systems_with_priority:
                        excess_consumption = system.consumption - max_consumption_by_priority[priority]
                        reduction = min(excess_consumption, remaining_consumption)
                        system.consumption -= reduction
                        remaining_consumption -= reduction
                        session.commit()
                        if remaining_consumption <= 0:
                            break
    
    # Espera de 5 segundos antes da próxima leitura dos sensores
    time.sleep(5)