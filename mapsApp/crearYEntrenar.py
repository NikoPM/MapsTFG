from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecExtractDictObs, VecMonitor, DummyVecEnv, VecEnvWrapper

from rl_routing.envs.vrpEnv import VRPEnv

import gymnasium as gym
import os
import time

"""
Definimos primero nombres de carpetas, para que se puedan crear en caso de no existir.
"""
def entrenarDesdeCero(algoritmo, modelName ,models_dir, log_dir, iterations = None, timesteps = None, nVehiculos = None, nNodos = None,):


     # Nombre de la ejecución (no afecta al algoritmo que se vaya a usar)
    models_dir = "temp/" + modelName # Directorio donde guardar los modelos generados
    log_dir = "temp"          # Directorios donde guardar los logs

    if not iterations:
        ITERATIONS = 1          # Número de iteraciones
    if not timesteps:
        TIMESTEPS = 2048*1       # Pasos por cada iteración (poner múltiplos de 2048)

    if not nVehiculos:
        nVehiculos = 7
    if not nNodos: 
        nNodos = 20

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


    """
    INICIALIZACIÓN DE ENTORNO Y AGENTE
    """

    # Para vectorizar el entorno y poder crear varios de manera paralela.
    # env = make_vec_env(VRPEnv, n_envs=1, env_kwargs=dict(nVehiculos = nVehiculos, nNodos = nNodos, maxNodeCapacity = 4, sameMaxNodeVehicles=True))
    env = gym.make('rl_routing:VRPEnv-v0',  nVehiculos = nVehiculos, nNodos = nNodos, maxNodeCapacity = 4, sameMaxNodeVehicles=True, render_mode=None)


    # Creamos el modelo. Se puede usar un algoritmo u otro simplemente cambiando el constructor
    # al correspondiente. Lo que hay dentro del constructor no hace falta cambiarlo.
    if algoritmo == "PPO":
        model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=log_dir)
        
    if algoritmo == "A2C":
        model = A2C("MultiInputPolicy", env, verbose=1, tensorboard_log=log_dir)
    
    """FALTA IMPLEMENTAR EL ALGORITMO DQN"""

    
    start_time = time.time()

    """
    ENTRENAMIENTO
    """
    for i in range(1, ITERATIONS+1):
        model.learn(total_timesteps = TIMESTEPS, reset_num_timesteps = False, tb_log_name = modelName)
        model.save(f"{models_dir}/{TIMESTEPS*i}")

    print("--- %s minutos ---" % round((time.time() - start_time)/60, 2))

    env.close()


    """
    Nota: usar el comando python crearYEntrenar.py >> log.txt 2>> errLog.txt para redirigir las salidas de prints/logs y errores.   
    """
