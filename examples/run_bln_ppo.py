"""
Original file:
https://raw.githubusercontent.com/openai/baselines/master/baselines/pposgd/run_mujoco.py
"""

#!/usr/bin/env python
from baselines.common import set_global_seeds, tf_util as U
from baselines import bench
import os.path as osp
import gym, logging
from baselines import logger
import sys
import tensorflow as tf
#import roboschool
from argparse import ArgumentParser

from cartpole_vrep_env import CartPoleVrepEnv

def train(max_time_in_s, seed):
	from baselines.pposgd import mlp_policy, pposgd_simple
	sess = U.make_session(num_cpu=1)
	sess.__enter__()
	logger.session().__enter__()
	set_global_seeds(seed)
	
	env = MartaVrepEnv();
	
	def policy_fn(name, ob_space, ac_space):
		return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space,
			hid_size=120, num_hid_layers=2)
	env = bench.Monitor(env, osp.join(logger.get_dir(), "monitor.json"))
	env.seed(seed)
	gym.logger.setLevel(logging.WARN)
	
	pposgd_simple.learn(env, policy_fn,
			#max_timesteps=num_timesteps,
			max_seconds= max_time_in_s,
			timesteps_per_batch=2048,
			clip_param=0.2, entcoeff=0.0,
			optim_epochs=10, optim_stepsize=3e-4, optim_batchsize=64,
			gamma=0.99, lam=0.95
		)
	env.close()
	saver = tf.train.Saver()
	saver.save(sess, '/tmp/model')

def main():
	train(max_time_in_s=((60*60)*12), seed=0)

if __name__ == "__main__":
	main()