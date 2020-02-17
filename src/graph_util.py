import os
import tarfile
import tensorflow as tf


def download_model(download_base, model_name, model_path):
    tf.keras.utils.get_file(model_path + ".tar.gz", download_base + model_name + ".tar.gz")
    tar_file = tarfile.open(model_path + '.tar.gz')

    if not os.path.isdir(model_path):
        os.makedirs(model_path)

    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.path.dirname(model_path))

    tar_file.close()


def load_graph(path):
    # Load model graph
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    return detection_graph