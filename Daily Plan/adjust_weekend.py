import pandas as pd

data = pd.read_csv('Daily Plan/adjust weekend.csv')

new_data = pd.DataFrame()
new_data['pid'] = data['pid'].copy()


def calculate_finish(start, period, dep, end):
    finish = start + period
    if (finish <= dep) or (start >= end):
        return [start, period, finish]
    elif start >= dep and finish <= end:
        return [0, 0, 0]
    elif start >= dep and start < end:
        start = end
        period = finish - end
        return [start, period, finish]
    elif finish > dep and finish <= end:
        finish = dep
        period = dep - start
        return [start, period, finish]


def adjust_activity_schedule(activities, dep, end):
    sorted_activities = sorted(activities, key=lambda x: x[0])

    for i in range(len(sorted_activities) - 1):
        current_activity = sorted_activities[i]
        next_activity = sorted_activities[i + 1]

        current_start, current_period, current_end = current_activity
        next_start, next_period, next_end = next_activity

        if next_end <= current_end:
            next_activity[0] = 0
            next_activity[1] = 0
            next_activity[2] = 0

        if current_end > next_start and next_end > current_end:
            overlap_duration = current_end - next_start
            adjust_time = overlap_duration // 2

            current_activity[1] -= adjust_time
            current_activity[2] -= adjust_time

            next_activity[1] -= adjust_time
            next_activity[0] += adjust_time

    return activities


unique_pids = data['pid'].unique()

for pid in unique_pids:
    df_subset = data[data['pid'] == pid]

    activities = []
    for index, row in df_subset.iterrows():
        activity = []
        for col in ['firstbath', 'secondbath', 'breakfast', 'lunch', 'dinner', 'washclothes', 'clean', 'footbath']:
            start_time = row[f'{col}happen1']
            period = row[f'{col}period1']
            activity.append([start_time, period, 0])

        for i, act in enumerate(activity):
            activity[i] = calculate_finish(act[0], act[1], row['weekend_deptime'], row['weekend_endtime'])

        adjusted_activities = adjust_activity_schedule(activity, row['weekend_deptime'], row['weekend_endtime'])

        for i, act in enumerate(adjusted_activities):
            col = ['firstbath', 'secondbath', 'breakfast', 'lunch', 'dinner', 'washclothes', 'clean', 'footbath'][i]
            new_data.loc[(new_data['pid'] == pid), f'{col}happen1'] = act[0]
            new_data.loc[(new_data['pid'] == pid), f'{col}period1'] = act[1]
            new_data.loc[(new_data['pid'] == pid), f'{col}end1'] = act[2]


new_data.to_csv('Daily Plan/adjust weekend new.csv', index=False)
