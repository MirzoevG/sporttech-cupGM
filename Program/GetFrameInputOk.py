import pandas as pd
import numpy as np
import math
import json


def GetInputFrame(data):
    data = pd.DataFrame(pd.json_normalize(data))

    # Будем возвращать этот фрейм, конечно внеся предварительно изменения
    sessions_frame = pd.DataFrame(pd.json_normalize(data['sessions'][0]))

    
    sessions_frame['samples_count'] = 0
    sessions_frame['samples_mean'] = 0
    sessions_frame['samples_std'] = 0
    sessions_frame['samples_min'] = 0
    sessions_frame['samples_max'] = 0
    
    sessions_frame['steps_diff_mean'] = 0
    sessions_frame['steps_diff_std'] = 0
    sessions_frame['steps_diff_min'] = 0
    sessions_frame['steps_diff_max'] = 0
    sessions_frame['steps_diff_q25'] = 0
    sessions_frame['steps_diff_q50'] = 0
    sessions_frame['steps_diff_q75'] = 0
    
    sessions_frame['steps_mean'] = 0
    sessions_frame['steps_std'] = 0
    sessions_frame['steps_min'] = 0
    sessions_frame['steps_max'] = 0
    sessions_frame['steps_q25'] = 0
    sessions_frame['steps_q50'] = 0
    sessions_frame['steps_q75'] = 0

    if 'active_artifacts' in sessions_frame.columns:
        sessions_frame = sessions_frame.drop('active_artifacts', axis=1)
    if not('skllzz_with_artifacts' in sessions_frame.columns):
        sessions_frame ['skllzz_with_artifacts'] = 0.0


    
    data['profile.sex'] = np.where(data['profile.sex'] == 'female', 0, 1)    
    
    data = data.rename(columns={'profile.birth_date' : 'birth_date'})
    data = data.rename(columns={'profile.sex' : 'sex'})
    data = data.rename(columns={'profile.weight' : 'weight'})

    
    sessions_frame['birth_date'] = data.at[0, 'birth_date']
    sessions_frame['hr'] = data.at[0, 'profile.hr_max'] - data.at[0, 'profile.hr_rest']
    sessions_frame.loc[:, 'weight'] = data.at[0, 'weight']
    sessions_frame.loc[:, 'sex'] = data.at[0, 'sex']

    for i in range(sessions_frame.shape[0]):
        # Здесь надо пройтись по каждой сессии и внести данные в session_frame
        steps_samples_frame = pd.DataFrame(pd.json_normalize(sessions_frame['steps.samples'][i]))
        steps_samples_frame = steps_samples_frame.astype({"stamp_millis" : 'int64'})


        sessions_frame['samples_count'].loc[i] = (((steps_samples_frame['stamp_millis'].diff()  - 900000.0)/60000).fillna(0)).describe()['count']
        sessions_frame['samples_mean'].loc[i] = (((steps_samples_frame['stamp_millis'].diff()  - 900000.0)/60000).fillna(0)).describe()['mean']
        sessions_frame['samples_std'].loc[i] = (((steps_samples_frame['stamp_millis'].diff()  - 900000.0)/60000).fillna(0)).describe()['std']
        sessions_frame['samples_min'].loc[i] = (((steps_samples_frame['stamp_millis'].diff()  - 900000.0)/60000).fillna(0)).describe()['min']
        sessions_frame['samples_max'].loc[i] = (((steps_samples_frame['stamp_millis'].diff()  - 900000.0)/60000).fillna(0)).describe()['max']
        
        sessions_frame['steps_diff_mean'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['mean']
        sessions_frame['steps_diff_std'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['std']
        sessions_frame['steps_diff_min'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['min']
        sessions_frame['steps_diff_max'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['max']
        sessions_frame['steps_diff_q25'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['25%']
        sessions_frame['steps_diff_q50'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['50%']
        sessions_frame['steps_diff_q75'].loc[i] = ((steps_samples_frame['steps'].diff()).fillna(0)).describe()['75%']

        sessions_frame['steps_mean'].loc[i] = steps_samples_frame['steps'].describe()['mean']
        sessions_frame['steps_std'].loc[i] = steps_samples_frame['steps'].describe()['std']
        sessions_frame['steps_min'].loc[i] = steps_samples_frame['steps'].describe()['min']
        sessions_frame['steps_max'].loc[i] = steps_samples_frame['steps'].describe()['max']
        sessions_frame['steps_q25'].loc[i] = steps_samples_frame['steps'].describe()['25%']
        sessions_frame['steps_q50'].loc[i] = steps_samples_frame['steps'].describe()['50%']
        sessions_frame['steps_q75'].loc[i] = steps_samples_frame['steps'].describe()['75%']
        

        

    
    del sessions_frame['id']
    del sessions_frame['start_millis']
    del sessions_frame['stop_millis']
    del sessions_frame['timezone']
    del sessions_frame['profile_id']
    del sessions_frame['activity_day']
    del sessions_frame['steps.day']
    del sessions_frame['steps.samples']

    sessions_frame = sessions_frame.rename(columns={'steps.steps' : 'steps'})
    sessions_frame = sessions_frame.rename(columns={'steps.meters' : 'meters'})

    sessions_frame['ratio_steps_meters'] = sessions_frame['steps'] / sessions_frame['meters']
    sessions_frame['cheater_value'] = 0

    new_column_order = ['skllzz', 'kkal', 'skllzz_without_artifacts', 'skllzz_with_artifacts', 'steps', 'meters', 'birth_date', 'hr', 'sex', 'weight', 'samples_count', 'samples_mean', 'samples_std', 'samples_min', 'samples_max', 'steps_diff_mean', 'steps_diff_std', 'steps_diff_min', 'steps_diff_max', 'steps_diff_q25', 'steps_diff_q50', 'steps_diff_q75', 'steps_mean', 'steps_std', 'steps_min', 'steps_max', 'steps_q25', 'steps_q50', 'steps_q75', 'ratio_steps_meters', 'cheater_value']
    sessions_frame = sessions_frame[new_column_order]
    
    return sessions_frame

    
