import copy
import matplotlib.pyplot as plt
import sys
sys.path.append("..")

import test.test_module.constants_for_experiments as ce
import tools.constants as c
import tools.utils as utils

def plot_people_clustering_experiments(
        yaml_paths, methods, params_list, plot_styles, inv_time, title=None):
    """
    Plot results of experiments on people clustering

    :type yaml_paths: list
    :param yaml_paths: paths of YAML files with experiment results

    :type methods: list
    :param methods: name of methods to be compared in the plots

    :type params_list: list
    :param params_list: parameters of methods to be compared in the plots

    :type plot_styles: list
    :param plot_styles: strings representing plot styles to be used

    :type inv_time: float
    :param inv_time: invariable analysis time

    :type title: string
    :param title: first part of title for all plots
    """
    # Load YAML files
    experiments_list = []

    # Check if there is at least one file path
    if len(yaml_paths) >= 1:

        dic1 = utils.load_YAML_file(yaml_paths[0])
        experiments_list = dic1[ce.EXPERIMENTS_KEY]

        for p in range(1, len(yaml_paths)):
            dic = utils.load_YAML_file(yaml_paths[p])
            experiments_list.extend(dic[ce.EXPERIMENTS_KEY])

    else:
        print('Warning! No YAML file paths provided')
        return

    if len(methods) != len(params_list):
        print('Warning! Length of methods and params_list is different')
        return

    if len(methods) != len(plot_styles):
        print('Warning! Length of methods and plot_styles is different')
        return

    # Set up dictionaries that will contain the results
    x_lists = {}
    prec_lists = {}
    rec_lists = {}
    f_measure_lists = {}
    time_lists = {}

    for i in range(0, len(methods)):

        x_lists[methods[i]] = []
        prec_lists[methods[i]] = []
        rec_lists[methods[i]] = []
        f_measure_lists[methods[i]] = []
        time_lists[methods[i]] = []

    for exp_extended in experiments_list:

        exp = exp_extended[ce.EXPERIMENT_KEY]

        nr_clusters = exp[c.PEOPLE_CLUSTERS_NR_KEY]  # Number of clusters
        prec = exp[ce.MEAN_PRECISION_KEY]  # Precision
        rec = exp[ce.MEAN_RECALL_KEY]  # Recall
        f_measure = exp[ce.MEAN_F1_KEY]  # F-measure
        # Time for creation of cloth models
        models_creation_time = exp[c.CLOTH_MODELS_CREATION_TIME_KEY]
        # Time for people clustering
        cluster_time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]
        time = inv_time + models_creation_time + cluster_time  # Total time

        conf_threshold = exp[c.CONF_THRESHOLD_KEY]
        video_name = exp[ce.VIDEO_NAME_KEY]
        use_aggr = exp[c.USE_AGGREGATION_KEY]
        use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]

        method_counter = 0
        for params in params_list:

            params_video_name = params[ce.VIDEO_NAME_KEY]
            # Add to all methods results with only face recognition
            if ((params_video_name == video_name) and (conf_threshold < 10)
                    and (not use_aggr) and (not use_clothing)):
                x_lists[methods[method_counter]].append(nr_clusters)
                prec_lists[methods[method_counter]].append(prec)
                rec_lists[methods[method_counter]].append(rec)
                f_measure_lists[methods[method_counter]].append(f_measure)
                time_lists[methods[method_counter]].append(time)
                method_counter += 1
                continue

            # Check equality of all given parameters
            all_equals = True
            for param in params.keys():

                if (param not in exp) or (params[param] != exp[param]):
                    all_equals = False

                    break

            if all_equals:
                print('nr_cluster', nr_clusters)
                print('precision', prec)
                x_lists[methods[method_counter]].append(nr_clusters)
                prec_lists[methods[method_counter]].append(prec)
                rec_lists[methods[method_counter]].append(rec)
                f_measure_lists[methods[method_counter]].append(f_measure)
                time_lists[methods[method_counter]].append(time)
                break

            method_counter += 1

    # Plot of precision
    method_counter = 0
    for method in methods:
        plt.plot(x_lists[method], prec_lists[method],
                 plot_styles[method_counter], label=method)
        method_counter += 1

    # Set plot
    title_str = 'Precision media al variare del numero di cluster'
    if title:
        title_str = title + ' - ' + title_str

    font_dict = {'fontsize': 12}  # Change font size
    plt.title(title_str, font_dict)

    plt.xlabel('Numero di cluster')
    plt.ylabel('Precision')
    plt.ylim([0, 1])
    plt.legend(bbox_to_anchor=(1, 0.34))
    plt.grid(True)

    plt.show()

    # Plot of recall
    method_counter = 0
    for method in methods:
        plt.plot(x_lists[method], rec_lists[method],
                 plot_styles[method_counter], label=method)
        method_counter += 1

    # Set plot
    title_str = 'Recall media al variare del numero di cluster'
    if title:
        title_str = title + ' - ' + title_str

    font_dict = {'fontsize': 12}  # Change font size
    plt.title(title_str, font_dict)

    plt.xlabel('Numero di cluster')
    plt.ylabel('Recall')
    plt.ylim([0, 1])
    plt.legend(bbox_to_anchor=(1, 0.34))
    plt.grid(True)

    plt.show()

    # Plot of f-measure
    method_counter = 0
    for method in methods:
        plt.plot(x_lists[method], f_measure_lists[method],
                 plot_styles[method_counter], label=method)
        method_counter += 1

    # Set plot
    title_str = '$F_1$ media al variare del numero di cluster'
    if title:
        title_str = title + ' - ' + title_str

    font_dict = {'fontsize': 12}  # Change font size
    plt.title(title_str, font_dict)

    plt.xlabel('Numero di cluster')
    plt.ylabel('$F_1$')
    plt.ylim([0, 1])
    plt.legend(bbox_to_anchor=(1, 0.34))
    plt.grid(True)

    plt.show()

    # Plot of time for analysis
    fig = plt.figure()
    ax = fig.add_subplot(111)
    method_counter = 0
    for method in methods:
        ax.plot(x_lists[method], time_lists[method],
                 plot_styles[method_counter], label=method)
        method_counter += 1

    # Set plot
    title_str = 'Tempo per il people clustering al variare del numero di cluster'
    if title:
        title_str = title + ' - ' + title_str

    font_dict = {'fontsize': 9}  # Change font size
    plt.title(title_str, font_dict)

    plt.xlabel('Numero di cluster')
    plt.ylabel('s')
    # plt.ylim([0, 25000])
    plt.legend(bbox_to_anchor=(0.76, 1))
    # plt.legend(bbox_to_anchor=(0.54, 1))
    plt.grid(True)

    # Set scientific notation
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.get_yaxis().major.formatter._useMathText = True

    plt.show()

yaml_paths = [r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-other-documents\Test\Face extraction\People clustering\Only face recognition\People_clustering_only_face_recognition.yml',
              r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-other-documents\Test\Face extraction\People clustering\Face + clothing recognition\People_clustering_face_plus_clothing_recognition.yml']

# 3 bboxes
# methods = ['Solo face recognition',
#            '2 x 1',
#            '2 x 2',
#            '2 x 1 - colore dominante',
#            '2 x 2 - colore dominante']

# mix fic.02
# methods = ['Solo face recognition',
#            '1 x 2 - bbox intero',
#            '2 x 2 - bbox intero + colore dominante',
#            '2 x 2 - 3 celle',
#            '2 x 2 - 3 celle + colore dominante']

# mix MONITOR072011
methods = ['Solo face recognition',
           '2 x 1 - bbox intero',
           '1 x 2 - bbox intero + colore dominante',
           '2 x 1 - 3 celle',
           '2 x 2 - 3 celle + colore dominante']

video_name = 'MONITOR072011.mpg'

only_face_recognition = {ce.VIDEO_NAME_KEY: video_name,
                         c.USE_CLOTHING_RECOGNITION_KEY: False,
                         c.USE_AGGREGATION_KEY: False}

face_clothing_rec_1_1 = {ce.VIDEO_NAME_KEY: video_name,
                         ce.CODE_VERSION_KEY: 328,
                         c.USE_CLOTHING_RECOGNITION_KEY: True,
                         c.CLOTHES_BBOX_WIDTH_KEY: 1.0,
                         c.CLOTHES_BBOX_HEIGHT_KEY: 1.0,
                         c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY: False,
                         c.CLOTHING_REC_USE_3_BBOXES_KEY: False
                         }

face_clothing_rec_2_1 = {ce.VIDEO_NAME_KEY: video_name,
                         ce.CODE_VERSION_KEY: 328,
                         c.USE_CLOTHING_RECOGNITION_KEY: True,
                         c.CLOTHES_BBOX_WIDTH_KEY: 2.0,
                         c.CLOTHES_BBOX_HEIGHT_KEY: 1.0,
                         c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY: False,
                         c.CLOTHING_REC_USE_3_BBOXES_KEY: False
                         }

face_clothing_rec_1_2 = {ce.VIDEO_NAME_KEY: video_name,
                         ce.CODE_VERSION_KEY: 328,
                         c.USE_CLOTHING_RECOGNITION_KEY: True,
                         c.CLOTHES_BBOX_WIDTH_KEY: 1.0,
                         c.CLOTHES_BBOX_HEIGHT_KEY: 2.0,
                         c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY: False,
                         c.CLOTHING_REC_USE_3_BBOXES_KEY: False
                         }

face_clothing_rec_2_2 = {ce.VIDEO_NAME_KEY: video_name,
                         ce.CODE_VERSION_KEY: 328,
                         c.USE_CLOTHING_RECOGNITION_KEY: True,
                         c.CLOTHES_BBOX_WIDTH_KEY: 2.0,
                         c.CLOTHES_BBOX_HEIGHT_KEY: 2.0,
                         c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY: False,
                         c.CLOTHING_REC_USE_3_BBOXES_KEY: False
                         }

face_clothing_rec_1_1_dom_color = copy.deepcopy(face_clothing_rec_1_1)
face_clothing_rec_1_1_dom_color[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = True

face_clothing_rec_2_1_dom_color = copy.deepcopy(face_clothing_rec_2_1)
face_clothing_rec_2_1_dom_color[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = True

face_clothing_rec_1_2_dom_color = copy.deepcopy(face_clothing_rec_1_2)
face_clothing_rec_1_2_dom_color[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = True

face_clothing_rec_2_2_dom_color = copy.deepcopy(face_clothing_rec_2_2)
face_clothing_rec_2_2_dom_color[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = True

face_clothing_rec_2_1_3_bboxes = copy.deepcopy(face_clothing_rec_2_1)
face_clothing_rec_2_1_3_bboxes[c.CLOTHING_REC_USE_3_BBOXES_KEY] = True

face_clothing_rec_2_2_3_bboxes = copy.deepcopy(face_clothing_rec_2_2)
face_clothing_rec_2_2_3_bboxes[c.CLOTHING_REC_USE_3_BBOXES_KEY] = True

face_clothing_rec_2_1_3_bboxes_dom_color = copy.deepcopy(
    face_clothing_rec_2_1_dom_color)
face_clothing_rec_2_1_3_bboxes_dom_color[c.CLOTHING_REC_USE_3_BBOXES_KEY] = True

face_clothing_rec_2_2_3_bboxes_dom_color = copy.deepcopy(
    face_clothing_rec_2_2_dom_color)
face_clothing_rec_2_2_3_bboxes_dom_color[c.CLOTHING_REC_USE_3_BBOXES_KEY] = True

params_list = [only_face_recognition,
               face_clothing_rec_1_1,
               face_clothing_rec_2_1,
               face_clothing_rec_1_2,
               face_clothing_rec_2_2]

params_list_dom_color = [only_face_recognition,
                         face_clothing_rec_1_1_dom_color,
                         face_clothing_rec_2_1_dom_color,
                         face_clothing_rec_1_2_dom_color,
                         face_clothing_rec_2_2_dom_color]

params_list_3_bboxes = [only_face_recognition,
                        face_clothing_rec_2_1_3_bboxes,
                        face_clothing_rec_2_2_3_bboxes,
                        face_clothing_rec_2_1_3_bboxes_dom_color,
                        face_clothing_rec_2_2_3_bboxes_dom_color]

params_list_mix_fic_02 = [only_face_recognition,
                          face_clothing_rec_1_2,
                          face_clothing_rec_2_2_dom_color,
                          face_clothing_rec_2_2_3_bboxes,
                          face_clothing_rec_2_2_3_bboxes_dom_color]

params_list_mix_MONITOR072011 = [only_face_recognition,
                                 face_clothing_rec_2_1,
                                 face_clothing_rec_1_2_dom_color,
                                 face_clothing_rec_2_1_3_bboxes,
                                 face_clothing_rec_2_2_3_bboxes_dom_color]

plot_styles = ['ks-',
               'g+--',
               'r*-.',
               'cv-',
               'bo:']

# For total analysis times: 18187.89 x fic.02, 39997.93 x MONITOR072011
inv_time = 0

title = 'MONITOR072011'

plot_people_clustering_experiments(
    yaml_paths, methods, params_list_mix_MONITOR072011, plot_styles, inv_time, title)

