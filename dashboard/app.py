import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

from pathlib import Path

sns.set_theme(style="whitegrid")

st.set_page_config(
    page_title="Police Fatalities in the United States",
    page_icon="📊",
    layout="wide"
)

st.title("Police Fatalities in the United States")

st.markdown(
    """
    ### Interactive Data Analysis Dashboard

    This dashboard explores recorded deaths involving police in the
    United States through **temporal, demographic, geographic, and
    incident-related patterns**.

    Use the filters in the sidebar to examine different subsets of
    the dataset and interact with the visualizations.
    """
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "canonical_cleaned_data.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
# Sidebar Filters

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filters")

st.sidebar.caption(
    "Use the filters below to explore different subsets of the dataset."
)

# Year
selected_years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].dropna().unique()),
    default=[]
)

# State
selected_states = st.sidebar.multiselect(
    "Select State",
    options=sorted(df["state"].dropna().unique()),
    default=[]
)

# Gender
selected_genders = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["gender"].dropna().unique()),
    default=[]
)

# Race
selected_races = st.sidebar.multiselect(
    "Select Race",
    options=sorted(df["race"].dropna().unique()),
    default=[]
)

# Age Group
age_group_order = [
    "<18",
    "18-25",
    "26-35",
    "36-45",
    "46-55",
    "56-65",
    "66+"
]

selected_age_groups = st.sidebar.multiselect(
    "Select Age Group",
    options=age_group_order,
    default=[]
)

# -----------------------------
# Apply Filters
# -----------------------------

filtered_df = df.copy()

if selected_years:
    filtered_df = filtered_df[
        filtered_df["year"].isin(selected_years)
    ]

if selected_states:
    filtered_df = filtered_df[
        filtered_df["state"].isin(selected_states)
    ]

if selected_genders:
    filtered_df = filtered_df[
        filtered_df["gender"].isin(selected_genders)
    ]

if selected_races:
    filtered_df = filtered_df[
        filtered_df["race"].isin(selected_races)
    ]

if selected_age_groups:
    filtered_df = filtered_df[
        filtered_df["age_group"].isin(selected_age_groups)
    ]

if any([
    selected_years,
    selected_states,
    selected_genders,
    selected_races,
    selected_age_groups
]):
    st.info(
        f"Showing {len(filtered_df):,} records based on the selected filters."
    )
else:
    st.info(
        f"Showing all {len(filtered_df):,} records in the dataset."
    )

total_fatalities = len(filtered_df)

average_age = filtered_df["age"].mean()

male_fatalities = (filtered_df["gender"] == "M").sum()

female_fatalities = (filtered_df["gender"] == "F").sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Fatalities", f"{total_fatalities:,}")

with col2:
    st.metric("Average Age", f"{average_age:.1f}")

with col3:
    st.metric("Male Fatalities", f"{male_fatalities:,}")

with col4:
    st.metric("Female Fatalities", f"{female_fatalities:,}")

# =========================
# Key Findings
# =========================

st.divider()

st.header("Key Findings")

# Largest age group
age_group_counts = (
    filtered_df["age_group"]
    .value_counts()
    .reindex(age_group_order)
    .dropna()
)

if not age_group_counts.empty:
    largest_age_group = age_group_counts.idxmax()
    largest_age_group_count = age_group_counts.max()
else:
    largest_age_group = "N/A"
    largest_age_group_count = 0


# Largest race category
race_counts = (
    filtered_df["race"]
    .value_counts()
    .dropna()
)

if not race_counts.empty:
    largest_race = race_counts.idxmax()
    largest_race_count = race_counts.max()
else:
    largest_race = "N/A"
    largest_race_count = 0


# Largest threat-level category
threat_counts = (
    filtered_df["threat_level"]
    .value_counts()
    .dropna()
)

if not threat_counts.empty:
    largest_threat = threat_counts.idxmax()
    largest_threat_count = threat_counts.max()
else:
    largest_threat = "N/A"
    largest_threat_count = 0


# Most common manner of death
manner_counts = (
    filtered_df["manner_of_death"]
    .value_counts()
    .dropna()
)

if not manner_counts.empty:
    most_common_manner = manner_counts.idxmax()
    most_common_manner_count = manner_counts.max()
else:
    most_common_manner = "N/A"
    most_common_manner_count = 0


# Median age
median_age = filtered_df["age"].median()

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        f"""
        **Age**

        Largest age group: **{largest_age_group}**

        **{largest_age_group_count:,}** recorded incidents
        """
    )

with col2:
    st.info(
        f"""
        **Largest Recorded Race Category**

        **{largest_race}** — **{largest_race_count:,}** recorded incidents
        """
    )

with col3:
    st.info(
        f"""
        **Largest Recorded Threat Category**

        **{largest_threat}** — **{largest_threat_count:,}** recorded incidents
        """
    )


col1, col2 = st.columns(2)

with col1:
    st.info(
        f"""
        **Manner of Death**

        **{most_common_manner}** — **{most_common_manner_count:,}** recorded incidents
        """
    )

with col2:
    if pd.notna(median_age):
        st.info(
            f"""
            **Age Statistics**

            Median recorded age: **{median_age:.0f} years**
            """
        )
    else:
        st.info(
            """
            **Age Statistics**

            Median recorded age: **N/A**
            """
        )

st.info(
    """
    **How to Read This Dashboard**

    The figures shown are counts of recorded incidents in the dataset.
    They should not be interpreted as population-adjusted rates or causal
    relationships. Use the sidebar filters to explore how the distributions
    change across different subsets of the data.
    """
)

st.divider()

yearly_counts = (
    filtered_df["year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

yearly_counts.columns = ["year", "fatalities"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fatalities Over Time")

    fig = px.line(
        yearly_counts,
        x="year",
        y="fatalities",
        markers=True,
        labels={
            "year": "Year",
            "fatalities": "Fatalities"
        }
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


with col2:
    st.subheader("Fatalities by Age Group")

    age_counts = (
        filtered_df["age_group"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_counts.columns = ["age_group", "fatalities"]

    fig = px.bar(
        age_counts,
        x="age_group",
        y="fatalities",
        labels={
            "age_group": "Age Group",
            "fatalities": "Fatalities"
        }
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()



monthly_counts = (
    filtered_df["month"]
    .value_counts()
    .sort_index()
    .reset_index()
)

monthly_counts.columns = ["month", "fatalities"]

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

monthly_counts["month_name"] = monthly_counts["month"].map(month_names)

fig = px.bar(
    monthly_counts,
    x="month_name",
    y="fatalities",
    labels={
        "month_name": "Month",
        "fatalities": "Fatalities"
    },
    title="Recorded Fatalities by Month"
)

fig.update_layout(
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis={
        "categoryorder": "array",
        "categoryarray": list(month_names.values())
    }
)

st.subheader("Fatalities by Month")

st.plotly_chart(
    fig,
    width="stretch"
)



st.divider()

st.header("Demographic Analysis")

gender_counts = (
    filtered_df["gender"]
    .value_counts()
    .reset_index()
)

gender_counts.columns = ["gender", "fatalities"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Gender")

    fig = px.bar(
        gender_counts,
        x="gender",
        y="fatalities",
        labels={
            "gender": "Gender",
            "fatalities": "Fatalities"
        }
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with col2:
    st.subheader("Race")

    race_counts = (
        filtered_df["race"]
        .value_counts()
        .dropna()
        .reset_index()
    )

    race_counts.columns = ["race", "fatalities"]

    fig = px.bar(
        race_counts,
        x="race",
        y="fatalities",
        labels={
            "race": "Race",
            "fatalities": "Fatalities"
        }
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()

st.header("Incident Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Threat Level")

    threat_counts = (
        filtered_df["threat_level"]
        .value_counts()
        .dropna()
        .reset_index()
    )

    threat_counts.columns = ["threat_level", "fatalities"]

    fig = px.bar(
        threat_counts,
        x="threat_level",
        y="fatalities",
        labels={
            "threat_level": "Threat Level",
            "fatalities": "Fatalities"
        },
        title="Fatalities by Threat Level"
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with col2:
    st.subheader("Manner of Death")

    manner_counts = (
        filtered_df["manner_of_death"]
        .value_counts()
        .dropna()
        .reset_index()
    )

    manner_counts.columns = ["manner_of_death", "fatalities"]

    fig = px.bar(
        manner_counts,
        x="manner_of_death",
        y="fatalities",
        labels={
            "manner_of_death": "Manner of Death",
            "fatalities": "Fatalities"
        },
        title="Manner of Death"
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()

st.header("Geographic Analysis")

state_counts = (
    filtered_df["state"]
    .value_counts()
    .head(15)
    .reset_index()
)

state_counts.columns = ["state", "fatalities"]

fig = px.bar(
    state_counts,
    x="fatalities",
    y="state",
    orientation="h",
    labels={
        "state": "State",
        "fatalities": "Fatalities"
    },
    title="Top 15 States by Recorded Fatalities"
)

fig.update_layout(
    margin=dict(l=20, r=20, t=50, b=20),
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

st.header("Dataset")

st.dataframe(
    filtered_df,
    width="stretch"
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="filtered_police_fatalities.csv",
    mime="text/csv"
)

st.divider()

st.header("About This Dashboard")

st.markdown(
    """
    ### Methodology

    The analysis uses a dataset containing recorded deaths involving
    police in the United States.

    The data was cleaned and prepared before visualization. Date fields
    were converted into usable datetime values, and additional features
    such as "year, month, day of the week, and age groups" were created.

    The dashboard allows users to explore the data using filters for:

    - Year
    - State
    - Gender
    - Race
    - Age Group

    All visualizations update dynamically based on the selected filters.
    """
)

st.subheader("Limitations")

st.markdown(
    """
    - The dataset represents recorded incidents available in the source
      data and should not be interpreted as a complete measure of all
      deaths involving police.
    - Missing values are present in some variables.
    - The analysis describes patterns in the dataset but does not establish
      causal relationships.
    - Counts should not be interpreted as population-adjusted rates unless
      population data is explicitly incorporated.
    """
)