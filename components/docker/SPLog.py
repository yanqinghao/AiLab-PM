# coding=utf-8
from __future__ import absolute_import, print_function

from pm4py.objects.conversion.log.factory import apply as df_to_log
from suanpan.app import app
from suanpan.app.arguments import Json, Csv
from utils.csv import convert_df_pm_format


@app.input(Csv(key="inputData1", alias="inputData"))
@app.output(Json(key="outputData1", alias="outputData"))
def SPLog(context):
    args = context.args
    df = convert_df_pm_format(args.inputData)
    log = df_to_log(df)
    replay = {"data": []}
    for event in log:
        event_name = event.attributes["concept:name"]
        for i, act in enumerate(event):
            if i < len(event) - 1:
                replay_act = {}
                replay_act["starttime"] = int(act["time:timestamp"].timestamp())
                replay_act["endtime"] = int(event[i + 1]["time:timestamp"].timestamp())
                replay_act["startact"] = act["concept:name"]
                replay_act["endact"] = event[i + 1]["concept:name"]
                replay_act["eventname"] = str(event_name)
                replay["data"].append(replay_act)
    return replay


if __name__ == "__main__":
    SPLog()
