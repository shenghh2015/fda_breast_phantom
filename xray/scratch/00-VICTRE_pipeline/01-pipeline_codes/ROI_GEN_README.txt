The ROI generation pipeline includes the following steps: Lesion insertion, X-ray imaging, DBT reconstruciton, ROI retraction. The configurations for the pipeline are shown below:
1. Install the packages needed for the lesion insertion, mc_gpu codes, and FBP reconstruction, and ROI reconstruction
2. Configure the directory to the lesion insertion python codes in the lesion_insertion.py
3. Configure the directory to mc_gpu commands (x-ray imaging), and x-ray configuration files for each type of phantom in the MCGPU.py
4. Configure the directory to FPB reconstruction command, command for concatenating input projections, and flatfield files in the DBTrecon.py
5. Configure the directory to ROI extraction python codes in the ROI_extraction.py


PS:
1. When compiling the FBP reconstruction, I add the phantom dataset folder as the input folder. The modified C codes are shared in the folder as well.
2. The lesion insertion and ROI extraction python codes were modified by me in order to aviod bugs, and the convenient for using these codes. The modifications are basically for the inputs of the codes. The modified codes are shared in the folder as well.
3. The concatenatioin commands compiled from C codes share by the FDA project authors. The codes and the comipled concatenation command is shared in the folder as well.

