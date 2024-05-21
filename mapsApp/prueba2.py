
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecExtractDictObs, VecMonitor, DummyVecEnv, VecEnvWrapper

from rl_routing.envs.vrpEnv import VRPEnv

import gymnasium as gym
import os
import time

"""
Definimos primero dónde buscar el modelo ya entrenado.
"""

model_name = "Models/Modelo_Caso_Farmacia/models/20480.zip"
models_dir = "temp" # Sin el -1 de las acciones, no funciona ni tan mal, pero tarda la vida. 
model_path = f"{models_dir}/{model_name}"

"""
INICIALIZACIÓN DE ENTORNO Y AGENTE
"""
nVehiculos = 3
nNodos = 8

env = gym.make('rl_routing:VRPEnv-v0',  nVehiculos, nNodos, maxNumVehiculos = nVehiculos, maxNumNodos=nNodos, maxNodeCapacity = 4, sameMaxNodeVehicles=False, render_mode='human', dataPath = 'C:/Users/Usuario/TFG/maps/MapsTFG/mapsApp/Cases/Caso Farmacias/')
#env.readEnvFromFile(nVehiculos = 5, nNodos = 15, maxVehicles = 7, maxNodos = 20, dataPath = 'data/')
env.reset()

model = PPO.load(model_path, env)
vec_env = model.get_env()

# Indicamos el número de episodios (a más episodios más soluciones obtendremos)
episodes = 1

start_time = time.time()

"""
GENERACIÓN DE RUTAS
"""
for ep in range(episodes):
    obs = vec_env.reset()
    done = False
    
    while not done:
        action, _ = model.predict(obs)

        obs, reward, done, info = vec_env.step(action)

    vec_env.render('human') # Guarda un report y los grafos en la ruta especificada.

    vec_env.close()