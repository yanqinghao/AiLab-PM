# coding=utf-8
from __future__ import absolute_import, print_function

import os
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.visualization.petrinet import factory as pn_vis_factory
from suanpan.app import app
from suanpan.app.arguments import Folder


@app.input(Folder(key="inputData1", alias="inputData"))
@app.output(Folder(key="outputData1", alias="outputData"))
def SPIMDFb(context):
    args = context.args
    inputFile = os.path.join(args.inputData, os.listdir(args.inputData)[0])
    log = xes_importer.import_log(inputFile)
    net, initial_marking, final_marking = inductive_miner.apply(log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    pn_vis_factory.save(gviz, os.path.join(args.outputData, "inductive-miner.png"))

    return args.outputData


if __name__ == "__main__":
    SPIMDFb()
