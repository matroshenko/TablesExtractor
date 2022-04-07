import os
# Turn off tensorflow warnings.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
tf.get_logger().setLevel('ERROR')


class ModelsManager(object):
    def __init__(self):
        models_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models'))
        detection_model_root_dir = os.path.join(models_root_dir, 'tables_detector_v3')

        self.detection_model = tf.saved_model.load(detection_model_root_dir).signatures['prediction_pipeline']

        analysis_model_root_dir = os.path.join(models_root_dir, 'splerge_model_v1')
        tf.load_op_library(os.path.join(analysis_model_root_dir, 'ops', 'ops.so'))

        self.analysis_model = tf.saved_model.load(analysis_model_root_dir).signatures['serving_default']

models_manager = ModelsManager()