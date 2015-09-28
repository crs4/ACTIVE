import os
import subprocess
import constants_for_experiments as ce
import tools.constants as c
from tools.utils import save_YAML_file

dataset_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-Sequences'
results_path = r'C:\Users\Maurizio\Documents\Risultati_test\Clothing_recognition'
video_name = 'SPALTI3_230907'

exps = range(-10, 20, 2)
exp_types = range(4, 6)

params = {
    c.CLOTHING_REC_HSV_CHANNELS_NR_KEY: 3,
    ce.CLOTHING_RECOGNITION_RESULTS_PATH_KEY: results_path,
    ce.VIDEO_NAME_KEY: video_name,
    ce.CLOTH_MODELS_DIR_PATH_KEY: results_path
}

for exp_type in exp_types:

    # Delete previously saved clothing models
    cloth_models_file_path = os.path.join(results_path, video_name)
    if os.path.exists(cloth_models_file_path):
        os.remove(cloth_models_file_path)

    if exp_type == 1:
        params[c.CLOTHING_REC_USE_LBP_KEY] = False
        params[c.CLOTHING_REC_USE_MASK_KEY] = False
        params[c.CLOTHING_REC_USE_MOTION_MASK_KEY] = False
    elif exp_type == 2:
        params[c.CLOTHING_REC_USE_LBP_KEY] = False
        params[c.CLOTHING_REC_USE_MASK_KEY] = True
        params[c.CLOTHING_REC_USE_MOTION_MASK_KEY] = False
    elif exp_type == 3:
        params[c.CLOTHING_REC_USE_LBP_KEY] = False
        params[c.CLOTHING_REC_USE_MASK_KEY] = False
        params[c.CLOTHING_REC_USE_MOTION_MASK_KEY] = True
    elif exp_type == 4:
        params[c.CLOTHING_REC_USE_LBP_KEY] = False
        params[c.CLOTHING_REC_USE_MASK_KEY] = True
        params[c.CLOTHING_REC_USE_MOTION_MASK_KEY] = True
    elif exp_type == 5:
        params[c.CLOTHING_REC_USE_LBP_KEY] = True
        params[c.CLOTHING_REC_USE_MASK_KEY] = False
        params[c.CLOTHING_REC_USE_MOTION_MASK_KEY] = False

    for exp in exps:
        k = 10 ** (exp / 10.0)
        print('k', k)

        params[c.CLOTHING_REC_K_KEY] = k

        params_file_path = r'C:\Users\Maurizio\Documents\Risultati_test\Clothing_recognition\clothing_recognition.yml'
        save_YAML_file(params_file_path, params)

        # # Launch subprocess

        command = ('python clothing_recognition_test.py -dataset_path ' +
                   dataset_path + ' -config ' + params_file_path)
        subprocess.call(command)
