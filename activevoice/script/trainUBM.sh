#!/bin/bash show="FabrizioGifuni-promessisposi-p1.wav"

# Input segmentation file, %s will be substituted with $show
seg="./%s.seg"

# Where is the mfcc, %s will be substituted with the name of the segment show fMask="./mfcc/%s.mfcc" 
# The MFCC vector description, here it corresponds to 12 MFCC + Energy
# spro4=the mfcc was computed by SPro4 tools 
# 1:1:0:0:0:0: 1 = present, 0 not present. 
# order : static, E, delta, delta E, delta delta delta delta E 
# 13: total size of a feature vector in the mfcc file 
# 1:0:0:1 CMS by cluster fDesc="spro4,1:1:0:0:0:0,13,1:0:0:1"

# The GMM used to initialize EM, %s will be substituted with $show
gmmInit="./%s.init.gmms" # The output GMM, %s will be substituted with $show
gmm="./%s.gmms"

# Initialize the UBM, ie a GMM with 8 diagonal Gaussian components
/usr/bin/java -Xmx1024m -cp ./LIUM_SpkDiarization.jar fr.lium.spkDiarization.programs.MTrainInit \
--sInputMask=$seg --fInputMask=$fMask --fInputDesc=$fDesc --kind=DIAG \
--nbComp=8 --emInitMethod=split_all --emCtrl=1,5,0.05 --tOutputMask=$gmmInit $show

# Train the UBM via EM
/usr/bin/java -Xmx1024m -cp ./LIUM_SpkDiarization.jar fr.lium.spkDiarization.programs.MTrainEM \
--sInputMask=$seg --fInputMask= $fMask --emCtrl=1,20,0.01 --fInputDesc=$fDesc \
--tInputMask=$gmmInit --tOutputMask=$gmm $show