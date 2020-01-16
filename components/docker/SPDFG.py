# coding=utf-8
from __future__ import absolute_import, print_function

from pm4py.algo.discovery.dfg import factory as dfg_miner
from pm4py.objects.conversion.log.factory import apply as df_to_log
from suanpan.app import app
from suanpan.app.arguments import Json, Csv, String
from utils.csv import convert_df_pm_format
from utils.dfg import dfg_vis


@app.input(Csv(key="inputData1", alias="inputData"))
@app.param(String(key="param1", alias="measure", default="frequency"))
@app.output(Json(key="outputData1", alias="outputData"))
def SPDFG(context):
    args = context.args
    df = convert_df_pm_format(args.inputData)
    log = df_to_log(df)
    dfg = dfg_miner.apply(log)
    outputData = dfg_vis(dfg, log=log, measure=args.measure)

    return outputData


if __name__ == "__main__":
    SPDFG()
