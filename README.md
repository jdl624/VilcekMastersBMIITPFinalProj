# VilcekMastersBMIITPFinalProj
How to Use Code

Begin by running cell 1 to import necessary packages

Run cell 2 to import the mock alzhiemers dataset as "data" and drop the unneccesary extra index column 
    You will see that this dataframe contains columns titled GDS, CDR, and various neuropsychological assessments with scores assigned for each row. These columns are the measures used to interpret a possible diagnosis.

Run cell 3 to calculate the z scores for each column. This will give us a better indication of if someone is cognitively impared. This also creates a new dataframe without the GDS, CDR, and seperate unprocessed neuropsych scores. Norms derived from this paper: https://files.alz.washington.edu/documentation/weintraub-2018-v3.pdf

Run cell 4 to create a normal (0) or abnormal (1) interpretation. All abnormal scores are defined as -1.5 standard deviations below the mean.

Run cell 5 to create a seperate series (dropping the z scores) of just the normal/abnormal score sums, this will be used in the initial clinical interpretation.

Run cell 6 to create the function alz_diagnose. This function (for now) interprets the combination of the GDS and CDR scores and spits out a possible diagnosis. (Will include the sum of abnormal neuropsych tests as well)

Run cell 7 to attach the newly created diagnosis list to the original "data" dataframe.

