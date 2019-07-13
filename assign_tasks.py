from datetime import datetime, timedelta
import json
from math import acos, cos, sin
import math

#data = '{ "batchId": "1562940000_50_5", "taskersCount": 5, "tasksCount": 50, "tasks": [{ "dueTime": "16:30", "lat": 48.85554319120794, "lng": 2.3613359633447204, "assignee_id": null, "id": 6480 }, { "dueTime": "13:15", "lat": 48.85313729018271, "lng": 2.32256080014798, "assignee_id": null, "id": 9297 }, { "dueTime": "21:45", "lat": 48.838453425693785, "lng": 2.372673134911582, "assignee_id": null, "id": 1889 } ] }'

TASKER_SPEED = 10  # km/h
EARTH_RADIUS = 6378  # km

def get_datetime(timestr):
    return datetime.strptime(timestr, '%H:%M')

def get_distance(task_a, task_b):
    """
    https://geodesie.ign.fr/contenu/fichiers/Distance_longitude_latitude.pdf
    """
    lat_a, lgn_a = task_a['lat'], task_a['lng']
    lat_b, lgn_b = task_b['lat'], task_b['lng']
    lat_a, lgn_a, lat_b, lgn_b =  [
        degree_angle * math.pi / 180 for degree_angle in [lat_a, lgn_a, lat_b, lgn_b]
    ]

    return EARTH_RADIUS * acos(sin(lat_a) * sin(lat_b) + cos(lat_a) * cos(lat_b) * cos(lgn_a - lgn_b))


def find_assignees(data):
    data = json.loads(data)
    ntaskers = data['taskersCount']

    tasks = data['tasks']  # list
    # sort by due time (gives a list (order))
    sorted_tasks = sorted(tasks, key=lambda d: get_datetime(d['dueTime']))  # O(Nlog(N))

    tasker_to_tasks = {}
    assigned_tasks = set()

    for i in range(ntaskers):  # O(M)
        tasker_id = i + 1
        tasker_to_tasks.setdefault(tasker_id, [])
        # select task due time whose duetime is the earliest
        for task in sorted_tasks:
            if task['id'] not in assigned_tasks:
                tasker_to_tasks[tasker_id].append(task['id'])
                assigned_tasks.add(task['id'])
                current_task = task
                break
        else:  # all tasks assigned
            break

        # compute "tasks schedule" according to the selected task
        # take into account travel time between locations
        for task in sorted_tasks:
            task_id = task['id']
            if task_id in assigned_tasks:
                continue
            task_duetime = get_datetime(task['dueTime'])
            travel_time = get_distance(current_task, task) / TASKER_SPEED
            endtime = get_datetime(current_task['dueTime']) + timedelta(minutes=30)
            task_mintime_arrival = endtime + timedelta(hours=travel_time)  # possible to use decimal hours

            if task_mintime_arrival <= task_duetime:  # select as next task
                tasker_to_tasks[tasker_id].append(task_id)
                assigned_tasks.add(task_id)
                current_task = task

    task_to_tasker = {}
    for tasker_id in tasker_to_tasks:
       for task_id in tasker_to_tasks[tasker_id]:
           task_to_tasker[task_id] = tasker_id

    for task in tasks:
        task['assignee_id'] = task_to_tasker.get(task['id'], None)  # None means the task is not assigned

    return data

if __name__ == '__main__':
    print(assign_tasks(data))
