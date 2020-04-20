import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')

#%matplotlib inline
print(tf.__version__)

from utils import label_map_util
from utils import visualization_utils as vis_util

MODEL_NAME = 'inference_graph'
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph_SSD_22_02_Detec4_30000.pb'
PATH_TO_LABELS = 'training/label_map_SSD_22_02_Detec4_30000.pbtxt'

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def run_inference_for_single_image(image, graph):
    if 'detection_masks' in tensor_dict:
        
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(             tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        
        tensor_dict['detection_masks'] = tf.expand_dims(             detection_masks_reframed, 0)
    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

    output_dict = sess.run(tensor_dict,feed_dict={image_tensor: np.expand_dims(image, 0)})

    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict[         'detection_classes'][0].astype(np.uint8)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]
    if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict

import cv2
cap = cv2.VideoCapture(0)

import datetime
from playsound import playsound
import subprocess
import sys

f = open("historico.txt","w+")

try:
    with detection_graph.as_default():
        with tf.Session() as sess:
                
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                  'num_detections', 'detection_boxes', 'detection_scores',
                  'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

                while True:       
                    ret, image_np = cap.read()
                    #Escrever a data no display
                    tempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    texto = "Sistema anti-drone - " + str(tempo)
                    org = (10, 20) 
                    thickness = 1
                    fontScale = 1
                    color = (0,255,0)
                    font = cv2.FONT_HERSHEY_COMPLEX_SMALL  
                    image_np = cv2.putText(image_np, texto, org, font, fontScale, color, thickness, cv2.LINE_AA)  
                    #print(tempo)
                    #print(frame)
                    
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    
                    output_dict = run_inference_for_single_image(image_np, detection_graph)
                    
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        output_dict['detection_boxes'],
                        output_dict['detection_classes'],
                        output_dict['detection_scores'],
                        category_index,
                        instance_masks=output_dict.get('detection_masks'),
                        use_normalized_coordinates=True,
                        line_thickness=8)
                    cv2.imshow('object_detection', cv2.resize(image_np, (800, 600)))                    
                                       
                    #para atribuir a uma variavel
                    if output_dict['detection_scores'][0] > 0.70 :
                    	#print(str(tempo), " - ", str(output_dict['detection_classes'][0] ) , ":" , str(output_dict['detection_scores'][0]))
                    	probabilidade = output_dict['detection_scores'][0] * 100
                    	#print(str(tempo), " - ", " Drone detectado!" , ":" , str(probabilidade), "%")
                    	#playsound('alarme.mp3')
                    	historico = str(tempo) + " - " + "Drone detectado!" + " : " + str(probabilidade) + "%" + '\n'
                    	f.write(historico)
                    	subprocess.Popen([sys.executable, "alarme_sript.py"]) # Call subprocess

                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        f.close() 
                        cap.release()
                        cv2.destroyAllWindows()
                        break

except Exception as e:
    print(e)
    cap.release()