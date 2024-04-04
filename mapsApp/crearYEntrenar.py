from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecExtractDictObs, VecMonitor, DummyVecEnv, VecEnvWrapper

from rl_routing.envs.vrpEnv import VRPEnv

import gymnasium as gym
import os
import time

"""
Definimos primero nombres de carpetas, para que se puedan crear en caso de no existir.
"""
def entrenarDesdeCero(algoritmo, models_dir, log_dir, iterations, timesteps, nVehiculos, nNodos):


     # Nombre de la ejecución (no afecta al algoritmo que se vaya a usar)
    ALGORITHM = models_dir + "/events"
    print(models_dir)
    models_dir += "/models"  # Directorio donde guardar los modelos generados
    print(models_dir)
    log_dir = models_dir + "/logs"    # Directorios donde guardar los logs

    ITERATIONS = iterations       # Número de iteraciones
    TIMESTEPS = timesteps*1       # Pasos por cada iteración (poner múltiplos de 2048)

    if not nVehiculos:
        nVehiculos = 7
    if not nNodos: 
        nNodos = 20
    print(f'{ITERATIONS, TIMESTEPS, nVehiculos, nNodos}')

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print('New path made')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print('New dir made')


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
    
    if algoritmo == "DQN":
        model = DQN("MultiInputPolicy", env, verbose=1, tensorboard_log=log_dir)

    
    start_time = time.time()

    """
    ENTRENAMIENTO
    """
    for i in range(1, ITERATIONS+1):
        model.learn(total_timesteps = TIMESTEPS, reset_num_timesteps = False, tb_log_name = ALGORITHM)
        model.save(f"{models_dir}/{TIMESTEPS*i}")

    print("--- %s minutos ---" % round((time.time() - start_time)/60, 2))

    env.close()


    """
    Nota: usar el comando python crearYEntrenar.py >> log.txt 2>> errLog.txt para redirigir las salidas de prints/logs y errores.   
    """
