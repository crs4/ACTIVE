import sys
sys.path.append("..")

import test.test_module.constants_for_experiments as ce
import tools.constants as c
import tools.utils as utils

def delete_experiments(file_path, save_file_path, params):
    """
    Delete experiments that do not match given parameters from given YAML file
    and save remaining experiments in new file

    :type file_path: string
    :param file_path: path of YAML file with experiment results

    :type save_file_path: string
    :param save_file_path: path of YAML file to be saved

    :type params: dictionary
    :param params: dictionary with parameters
    """

    dic = utils.load_YAML_file(file_path)
    experiment_list = dic[ce.EXPERIMENTS_KEY]

    new_experiment_list = []

    print('len(experiment_list)', len(experiment_list))

    for exp_extended in experiment_list:

        exp = exp_extended[ce.EXPERIMENT_KEY]

        all_equals = True
        for param in params.keys():

            if (param not in exp) or (params[param] != exp[param]):
                all_equals = False
                break

        # Add experiment to new list only if all experiment parameters
        # equals those from given dictionary with parameters
        if all_equals:
            exp_extended[ce.EXPERIMENT_KEY][c.LEV_RATIO_PCT_THRESH_KEY] = float(exp[c.LEV_RATIO_PCT_THRESH_KEY])
            new_experiment_list.append(exp_extended)

    # Save new YAML file
    print('len(new_experiment_list)', len(new_experiment_list))
    new_dic = {ce.EXPERIMENTS_KEY: new_experiment_list}
    utils.save_YAML_file(save_file_path, new_dic)

#file_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1800-.yml'
file_path = r'C:\Active\Risultati test\People recognition\People_recognition.yml'

#save_file_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-other-documents\Test\Face extraction\People clustering\Face + clothing recognition\People_clustering_face_plus_clothing_recognition.yml'
save_file_path = r'C:\Active\Risultati test\People recognition\People_recognition-SPALTI3_230907.yml'

params = {ce.VIDEO_NAME_KEY: 'SPALTI3_230907.mpg'}

delete_experiments(file_path, save_file_path, params)

