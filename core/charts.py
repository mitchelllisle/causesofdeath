import altair as alt
import numpy as np
# import os
# os.chdir("/Users/mitchell/Documents/projects/causesofdeath")


def return_vega_spec_json(chart):
    return chart.to_json().replace("\n", "").strip()


def calcRateOfChange(x):
    data = x.sort_values("year")
    data['pct_change'] = ((data['count'].pct_change()) * 100)
    return data


def roc_chart(data, category):
    mbd = data[data['chapter'] == category]

    chartData = mbd.groupby(["cause_of_death_map", "sex", "year"]).agg({"count": "sum"}).reset_index().sort_values("count", ascending=False)

    output = (
        chartData[chartData['year'].isin(['2008', '2017'])]
        .groupby(['cause_of_death_map', 'sex'])
        .apply(lambda x: calcRateOfChange(x))
        .reset_index(drop=True)
    )

    output = output.replace([np.inf, -np.inf], np.nan).dropna()[['cause_of_death_map', 'sex', 'pct_change']]

    output = output.assign(pct_change=output['pct_change'].map(int))

    males = output[(output['sex'] == 'Males') & (output['pct_change'] > 0)].sort_values("pct_change", ascending=False).to_dict(orient="records")
    females = output[(output['sex'] == 'Females') & (output['pct_change'] > 0)].sort_values("pct_change", ascending=False).to_dict(orient="records")

    return {"males": males, "females": females}


def timeseries_chart(data, category):
    chartData = (
        data[data['chapter'] == category]
        .groupby(["cause_of_death_map", "sex", "year"])
        .agg({"count": "sum"})
        .reset_index()
        .sort_values("count", ascending=False)
    )

    colorScale = alt.Scale(
        domain=['Males', 'Females'],
        range=['#4A90E2', '#50E3C2']
    )

    choices = chartData[chartData['cause_of_death_map'] != 'Other']['cause_of_death_map'].unique()

    colorScale = alt.Scale(
        domain=['Males', 'Females'],
        range=['#4A90E2', '#50E3C2']
    )

    base = alt.Chart(chartData).mark_line(
        point=True,
        interpolate="cardinal"
    ).encode(
        x=alt.X("year", type="nominal", axis=alt.Axis(labelAngle=330), title="Year"),
        y=alt.Y("count", title="Number of Deaths"),
        tooltip=chartData.columns.tolist(),
        color=alt.Color("sex", scale=colorScale, legend=alt.Legend(title="Gender"))
    ).properties(
        width=350,
        height=200
    )

    one = base.transform_filter(
        alt.FieldEqualPredicate(field='cause_of_death_map', equal=choices[0])
    ).properties(
        title=choices[0]
    )

    two = base.transform_filter(
        alt.FieldEqualPredicate(field='cause_of_death_map', equal=choices[1])
    ).properties(
        title=choices[1]
    )

    three = base.transform_filter(
        alt.FieldEqualPredicate(field='cause_of_death_map', equal=choices[2])
    ).properties(
        title=choices[2]
    )

    chart = alt.hconcat(one, two, three).configure(
        axis=alt.Axis(grid=False)
    )
    return return_vega_spec_json(chart)


def external_causes_category_chart(data):
    ed = data[data['chapter'] == 'External causes of morbidity and mortality']

    causeCounts = (
        ed
        .groupby("cause_of_death_map")
        .agg({"count": "sum"})
        .reset_index()
        .sort_values("count", ascending=False)
        .head(10)
    )

    alt.Chart(causeCounts).mark_bar(color="orange").encode(
        y=alt.Y("cause_of_death_map", sort=alt.SortField("sum", "count", order="descending")),
        x=alt.X("count"),
        tooltip=causeCounts.columns.tolist()
    ).properties(
        width=800,
        height=400
    )
