#!/usr/bin/env python3
import tensorflow as tf
import time
from pprint import pprint
s = time.time()
print(f"tf version: {tf.__version__}")
pprint(tf.sysconfig.get_build_info())
print(tf.config.list_physical_devices())
print(f"Took {round(time.time() - s)}s")