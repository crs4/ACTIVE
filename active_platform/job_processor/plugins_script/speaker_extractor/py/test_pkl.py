import pickle
from voiceid.sr import Cluster
if __name__ == '__main__':
    pkl_path="/Users/labcontenuti/Music/facciamo_i_conti_internet.wav.pkl"
    cluster  = pickle.load( open( pkl_path, "rb" ) )
    print cluster
    for k in cluster.keys():
        print k, " duration=", cluster[k].get_duration(), " best five=", cluster[k].get_best_five()
        print "."
        