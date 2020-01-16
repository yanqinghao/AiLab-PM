from copy import copy

from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.dfg.utils import dfg_utils
from pm4py.objects.log.util import xes
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY
from pm4py.visualization.common.utils import human_readable_stat


def dfg_vis(dfg, log=None, parameters=None, activities_count=None, measure="frequency"):
    if parameters is None:
        parameters = {}

    activity_key = (
        parameters[PARAMETER_CONSTANT_ACTIVITY_KEY]
        if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters
        else xes.DEFAULT_NAME_KEY
    )

    max_no_of_edges_in_diagram = 75

    if "maxNoOfEdgesInDiagram" in parameters:
        max_no_of_edges_in_diagram = parameters["maxNoOfEdgesInDiagram"]

    start_activities = (
        parameters["start_activities"] if "start_activities" in parameters else []
    )
    end_activities = (
        parameters["end_activities"] if "end_activities" in parameters else []
    )

    if activities_count is None:
        if log is not None:
            activities_count = attributes_filter.get_attribute_values(
                log, activity_key, parameters=parameters
            )
        else:
            activities = dfg_utils.get_activities_from_dfg(dfg)
            activities_count = {key: 1 for key in activities}

    return graphviz_visualization(
        activities_count,
        dfg,
        measure=measure,
        max_no_of_edges_in_diagram=max_no_of_edges_in_diagram,
        start_activities=start_activities,
        end_activities=end_activities,
    )


def graphviz_visualization(
    activities_count,
    dfg,
    measure="frequency",
    max_no_of_edges_in_diagram=170,
    start_activities=None,
    end_activities=None,
):
    """
    Do GraphViz visualization of a DFG graph

    Parameters
    -----------
    activities_count
        Count of attributes in the log (may include attributes that are not in the DFG graph)
    dfg
        DFG graph
    image_format
        GraphViz should be represented in this format
    measure
        Describes which measure is assigned to edges in direcly follows graph (frequency/performance)
    max_no_of_edges_in_diagram
        Maximum number of edges in the diagram allowed for visualization

    Returns
    -----------
    node_edge_data
        node and edge dict data
    """
    if start_activities is None:
        start_activities = []
    if end_activities is None:
        end_activities = []

    # first, remove edges in diagram that exceeds the maximum number of edges in the diagram
    dfg_key_value_list = []
    for edge in dfg:
        dfg_key_value_list.append([edge, dfg[edge]])
    dfg_key_value_list = sorted(dfg_key_value_list, key=lambda x: x[1], reverse=True)
    dfg_key_value_list = dfg_key_value_list[
        0 : min(len(dfg_key_value_list), max_no_of_edges_in_diagram)
    ]
    dfg_allowed_keys = [x[0] for x in dfg_key_value_list]
    dfg_keys = list(dfg.keys())
    for edge in dfg_keys:
        if edge not in dfg_allowed_keys:
            del dfg[edge]

    activities_in_dfg = set()
    activities_count_int = copy(activities_count)

    for edge in dfg:
        activities_in_dfg.add(edge[0])
        activities_in_dfg.add(edge[1])

    if len(activities_in_dfg) == 0:
        activities_to_include = set(activities_count_int)
    else:
        activities_to_include = set(activities_in_dfg)

    node_edge_data = {"nodes": [], "edges": []}

    for act in activities_to_include:
        if "frequency" in measure and act in activities_count_int:
            node_edge_data["nodes"].append(
                {"data": {"id": act, "label": activities_count_int[act]}}
            )
        else:
            node_edge_data["nodes"].append({"data": {"id": act, "label": None}})

    # represent edges
    for edge in dfg:
        if "frequency" in measure:
            label = str(dfg[edge])
        else:
            label = human_readable_stat(dfg[edge])
        node_edge_data["edges"].append(
            {"data": {"source": edge[0], "target": edge[1], "id": label}}
        )

    return node_edge_data


def get_min_max_value(dfg):
    """
    Gets min and max value assigned to edges
    in DFG graph

    Parameters
    -----------
    dfg
        Directly follows graph

    Returns
    -----------
    min_value
        Minimum value in directly follows graph
    max_value
        Maximum value in directly follows graph
    """
    min_value = 9999999999
    max_value = -1

    for edge in dfg:
        if dfg[edge] < min_value:
            min_value = dfg[edge]
        if dfg[edge] > max_value:
            max_value = dfg[edge]

    return min_value, max_value

