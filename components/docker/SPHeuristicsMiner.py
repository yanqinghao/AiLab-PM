# coding=utf-8
from __future__ import absolute_import, print_function

import os
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.heuristics import factory as heuristics_miner
from pm4py.visualization.heuristics_net import factory as hn_vis_factory
from suanpan.app import app
from suanpan.app.arguments import Folder, Float, Int


@app.input(Folder(key="inputData1", alias="inputData"))
@app.param(Float(key="dependencyThresh", default=0.5))
@app.param(Float(key="andMeasureThresh", default=0.65))
@app.param(Int(key="minActCount", default=1))
@app.param(Int(key="minDfgOccurrences", default=1))
@app.param(Float(key="dfgPreCleaningNoiseThresh", default=0.05))
@app.output(Folder(key="outputData1", alias="outputData"))
def SPHeuristicsMiner(context):
    args = context.args
    inputFile = os.path.join(args.inputData, os.listdir(args.inputData)[0])
    log = xes_importer.import_log(inputFile)
    heu_net = heuristics_miner.apply_heu(
        log,
        parameters={
            "dependency_thresh": args.dependencyThresh,
            "and_measure_thresh": args.andMeasureThresh,
            "min_act_count": args.minActCount,
            "min_dfg_occurrences": args.minDfgOccurrences,
            "dfg_pre_cleaning_noise_thresh": args.dfgPreCleaningNoiseThresh,
        },
    )
    gviz = hn_vis_factory.apply(heu_net)
    hn_vis_factory.save(gviz, os.path.join(args.outputData, "heuristics-miner.png"))

    return args.outputData


if __name__ == "__main__":
    SPHeuristicsMiner()
