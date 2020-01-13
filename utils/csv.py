from pm4py.objects.log.adapters.pandas.csv_import_adapter import (
    convert_timestamp_columns_in_df,
)


def convert_df_pm_format(
    df,
    sort=False,
    sort_field="time:timestamp",
    timest_format=None,
    timest_columns=None,
):
    df = convert_timestamp_columns_in_df(
        df, timest_format=timest_format, timest_columns=timest_columns
    )
    if sort and sort_field:
        df = df.sort_values(sort_field)
    return df
