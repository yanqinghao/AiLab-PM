# coding=utf-8
from __future__ import absolute_import, print_function

import os
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.objects.petri.exporter import pnml as pnml_exporter
from suanpan.app import app
from suanpan.app.arguments import Folder, Csv
from utils.csv import convert_df_pm_format


@app.input(Csv(key="inputData1", alias="inputData"))
@app.output(Folder(key="outputData1", alias="outputData"))
def SPAlphaMiner(context):
    args = context.args
    log = convert_df_pm_format(args.inputData)
    net, initial_marking, final_marking = alpha_miner.apply(log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    pn_vis_factory.save(gviz, os.path.join(args.outputData, "alpha-miner.png"))
    pnml_exporter.export_net(
        net,
        initial_marking,
        os.path.join(args.outputData, "petri_final.pnml"),
        final_marking=final_marking,
    )

    return args.outputData


if __name__ == "__main__":
    SPAlphaMiner()
