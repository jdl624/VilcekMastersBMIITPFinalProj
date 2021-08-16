import pandas as pd
import numpy as np
import os
import shutil

class AlzDiagnosisAlg():
    
    def open_dataframe(file_path):
        #Opens .csv file
        if file_path.endswith('csv'):
            df = pd.read_csv(file_path)
            df = df.drop(columns = 'Unnamed: 0')
        else:
            raise ValueError('File is not in proper .csv format')
        return df
    
    def z_calc(data):
        # calculates z scores for each neuropsych test based on norms derived from this paper: https://files.alz.washington.edu/documentation/weintraub-2018-v3.pdf
        zs = data
        for row in range(zs.shape[0]):
            if zs.iloc[row, 1] < 60:
                zs = zs.assign(Delayed_Recall_Z = lambda x: ((x['Delayed Recall']-20.9)/7.0))
                zs = zs.assign(Number_Span_Test_Forward_Z = lambda x: ((x['Number Span Test Forward']-8.7)/2.4))
                zs = zs.assign(Part_A_Trail_Making_Z = lambda x: ((-x['Part A Trail Making']+22.3)/8.4))
                zs = zs.assign(Part_B_Trail_Making_Z = lambda x: ((-x['Part B Trail Making']+55.4)/27.2))
                zs = zs.assign(MoCA_Z = lambda x: ((x['moca']-27.5)/2.1))
                zs = zs.assign(Categories_Animal_Z = lambda x: ((x['Categories Animal']-23.6)/5.3))
            if 60 <= zs.iloc[row, 1] <= 69:
                zs = zs.assign(Delayed_Recall_Z = lambda x: ((x['Delayed Recall']-20.4)/6.4))
                zs = zs.assign(Number_Span_Test_Forward_Z = lambda x: ((x['Number Span Test Forward']-8.4)/2.3))
                zs = zs.assign(Part_A_Trail_Making_Z = lambda x: ((-x['Part A Trail Making']+27.3)/9.6))
                zs = zs.assign(Part_B_Trail_Making_Z = lambda x: ((-x['Part B Trail Making']+70.1)/33.8))
                zs = zs.assign(MoCA_Z = lambda x: ((x['moca']-26.9)/2.4))
                zs = zs.assign(Categories_Animal_Z = lambda x: ((x['Categories Animal']-22.7)/5.5))
            if 70 <= zs.iloc[row, 1] <= 79:
                zs = zs.assign(Delayed_Recall_Z = lambda x: ((x['Delayed Recall']-26.3)/2.7))
                zs = zs.assign(Number_Span_Test_Forward_Z = lambda x: ((x['Number Span Test Forward']-8.3)/2.3))
                zs = zs.assign(Part_A_Trail_Making_Z = lambda x: ((-x['Part A Trail Making']+31.0)/10.8))
                zs = zs.assign(Part_B_Trail_Making_Z = lambda x: ((-x['Part B Trail Making']+82.7)/41.4))
                zs = zs.assign(MoCA_Z = lambda x: ((x['moca']-26.3)/2.7))
                zs = zs.assign(Categories_Animal_Z = lambda x: ((x['Categories Animal']-21.2)/5.4))
            if 80 <= zs.iloc[row, 1] <= 89:
                zs = zs.assign(Delayed_Recall_Z = lambda x: ((x['Delayed Recall']-16.9)/6.6))
                zs = zs.assign(Number_Span_Test_Forward_Z = lambda x: ((x['Number Span Test Forward']-8.0)/2.3))
                zs = zs.assign(Part_A_Trail_Making_Z = lambda x: ((-x['Part A Trail Making']+36.2)/13.3))
                zs = zs.assign(Part_B_Trail_Making_Z = lambda x: ((-x['Part B Trail Making']+102.0)/55.2))
                zs = zs.assign(MoCA_Z = lambda x: ((x['moca']-25.3)/3.0))
                zs = zs.assign(Categories_Animal_Z = lambda x: ((x['Categories Animal']-19.5)/5.6))
            if 90 <= zs.iloc[row, 1]:
                zs = zs.assign(Delayed_Recall_Z = lambda x: ((x['Delayed Recall']-15.1)/5.8))
                zs = zs.assign(Number_Span_Test_Forward_Z = lambda x: ((x['Number Span Test Forward']-7.6)/2.1))
                zs = zs.assign(Part_A_Trail_Making_Z = lambda x: ((-x['Part A Trail Making']+42.0)/13.4))
                zs = zs.assign(Part_B_Trail_Making_Z = lambda x: ((-x['Part B Trail Making']+140.6)/75.3))
                zs = zs.assign(MoCA_Z = lambda x: ((x['moca']-23.8)/3.5))
                zs = zs.assign(Categories_Animal_Z = lambda x: ((x['Categories Animal']-17.0)/5.4))
            zs = zs.drop(['Age', 'CDR','Delayed Recall','Number Span Test Forward','Part A Trail Making','Part B Trail Making','moca','Categories Animal'], axis = 1)
            
            zs_ab = zs
            zs_ab['DR_ab'] = zs_ab['Delayed_Recall_Z'].apply(lambda x: 1 if x <= -1.5 else 0)
            zs_ab['NSF_ab'] = zs_ab['Number_Span_Test_Forward_Z'].apply(lambda x: 1 if x <= -1.5 else 0)
            zs_ab['TMA_ab'] = zs_ab['Part_A_Trail_Making_Z'].apply(lambda x: 1 if x <= -1.5 else 0)
            zs_ab['TMB_ab'] = zs_ab['Part_B_Trail_Making_Z'].apply(lambda x: 1 if x <= -1.5 else 0)
            zs_ab['MoCA_ab'] = zs_ab['MoCA_Z'].apply(lambda x: 1 if x <= -1.5 else 0)
            zs_ab['Cat_An_ab'] = zs_ab['Categories_Animal_Z'].apply(lambda x: 1 if x <= -1.5 else 0)
            zs_ab = zs_ab.drop(['Delayed_Recall_Z','Number_Span_Test_Forward_Z','Part_A_Trail_Making_Z','Part_B_Trail_Making_Z','MoCA_Z','Categories_Animal_Z'], axis = 1)
            return zs_ab

    
    def alz_diagnose(data):
        #Assigns diagnosis based off GDS and CDR values.
        data = data.drop(['Age', 'Delayed Recall','Number Span Test Forward','Part A Trail Making','Part B Trail Making','moca','Categories Animal'], axis = 1)
        diags = []
        for row in range(data.shape[0]):
            row_sum = data.iloc[row].sum()
            try:
                if row_sum <= 0.5:
                    raise ValueError()
                elif 1.0 <= row_sum <= 2.0:
                    if data.iloc[row, 0] == 1:
                        diags.append('Normal')
                    if data.iloc[row, 0] == 2:
                        diags.append('SCD')
                elif row_sum == 3.5:
                    diags.append('MCI')
                elif row_sum <= 5:
                    diags.append('Probable Dementia')
                elif 6 <= row_sum <= 7:
                    diags.append('Mild Dementia')
                elif 8 <= row_sum <= 9:
                    diags.append('Moderate Dementia')
                elif row_sum == 10:
                    diags.append('Severe Dementia')
                elif row_sum >= 10.5:
                    raise ValueError()
                else:
                    raise ValueError()
            except ValueError:
                diags.append('These diagnostic values are out of range. Please verify values are correct.')
                pass
        return diags
    
    def abnormal_zs(zs_ab):
        cognition = []
        for row in range(zs_ab.shape[0]):
            try:
                if 3<= zs_ab.iloc[row, 0] <= 7:
                    zs_ab_dropped = zs_ab.drop(['GDS'], axis = 1)
                    row_sum = zs_ab_dropped.iloc[row].sum()
                    if row_sum == 0:
                        cognition.append('Normal Cognition')
                    if row_sum == 1:
                        cognition.append('Single Domain Deficient')
                    if row_sum >= 2:
                        cognition.append('Multiple Domains Deficient')
                elif 1<= zs_ab.iloc[row, 0] <= 2:
                    cognition.append('Not Cognitively Impaired')
                else:
                    raise ValueError()
            except ValueError:
                cognition.append('Invalid GDS Value, must be between 1 and 7')
                pass 
        return cognition
    
    def cognitive_domains(zs_ab):
        domains = []
        for row in range(zs_ab.shape[0]):
            try:
                if 1<= zs_ab.iloc[row, 0] <= 2:
                    domains.append('Normal Cognition')
                elif 3<= zs_ab.iloc[row, 0] <= 7:
                    zs_ab_dropped = zs_ab.drop(['GDS'], axis = 1)
                    row_sum = zs_ab_dropped.iloc[row].sum()
                    if row_sum == 0:
                        domains.append('Normal Cognition')
                    if row_sum == 1:
                        if zs_ab_dropped.iloc[row, 0]==1:
                            domains.append('Memory')
                        if zs_ab_dropped.iloc[row, 1]==1:
                            domains.append('Attention')
                        if zs_ab_dropped.iloc[row, 2]==1:
                            domains.append('Processing speed')
                        if zs_ab_dropped.iloc[row, 3]==1:
                            domains.append('Executive Function')
                        if zs_ab_dropped.iloc[row, 4]==1:
                            domains.append('Dementia severity')
                        if zs_ab_dropped.iloc[row, 5]==1:
                            domains.append('Lang. category fluency')
                        else:
                            pass
                    if row_sum >= 2:
                        sub_domains = []
                        if zs_ab_dropped.iloc[row, 0]==1:
                            sub_domains.append('Memory')
                        if zs_ab_dropped.iloc[row, 1]==1:
                            sub_domains.append('Attention')
                        if zs_ab_dropped.iloc[row, 2]==1:
                            sub_domains.append('Processing speed')
                        if zs_ab_dropped.iloc[row, 3]==1:
                            sub_domains.append('Executive Function')
                        if zs_ab_dropped.iloc[row, 4]==1:
                            sub_domains.append('Dementia severity')
                        if zs_ab_dropped.iloc[row, 5]==1:
                            sub_domains.append('Lang. category fluency')
                        else:
                            pass
                        domains.append(sub_domains)
                else:
                    raise ValueError()
            except ValueError:
                domains.append('Values could not be parsed')
                pass    
        return domains
    def run_all(file_path):
        data = AlzDiagnosisAlg.open_dataframe(file_path)
        zs_interp = AlzDiagnosisAlg.z_calc(data)
        diags = AlzDiagnosisAlg.alz_diagnose(data)
        cognition = AlzDiagnosisAlg.abnormal_zs(zs_interp)
        domains = AlzDiagnosisAlg.cognitive_domains(zs_interp)
        
        data = data.drop(['Delayed Recall','Number Span Test Forward','Part A Trail Making','Part B Trail Making','moca','Categories Animal'], axis = 1)
        df5 = pd.DataFrame({'Cognition':cognition, "Cognitive Domains":domains, 'Diagnosis':diags})
        data = data.join(df5)
        
        name,ext = os.path.splitext(file_path)
        data.to_csv(name+'_diag'+ext)
        
        original = r'/Users/jonlinks/Documents/VilcekMastersBMIITPFinalProj/alz_data_diag.csv'
        target = r'/Users/jonlinks/Documents/VilcekMastersBMIITPFinalProj/Results/alz_data_diag.csv'
        shutil.move(original,target)
        return data