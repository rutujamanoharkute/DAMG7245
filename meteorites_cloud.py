!pip install -U pandas-profiling

"""### Import libraries"""

import numpy as np
import pandas as pd

import ydata_profiling
from ydata_profiling.utils.cache import cache_file

"""### Load and prepare example dataset
We add some fake variables for illustrating pandas-profiling capabilities
"""

file_name = cache_file(
    "meteorites.csv",
    "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD",
)

df = pd.read_csv(file_name)

# Note: Pandas does not support dates before 1880, so we ignore these for this analysis
df["year"] = pd.to_datetime(df["year"], errors="coerce")

# Example: Constant variable
df["source"] = "NASA"

# Example: Boolean variable
df["boolean"] = np.random.choice([True, False], df.shape[0])

# Example: Mixed with base types
df["mixed"] = np.random.choice([1, "A"], df.shape[0])

# Example: Highly correlated variables
df["reclat_city"] = df["reclat"] + np.random.normal(scale=5, size=(len(df)))

# Example: Duplicate observations
duplicates_to_add = pd.DataFrame(df.iloc[0:10])
duplicates_to_add["name"] = duplicates_to_add["name"] + " copy"

df = df.append(duplicates_to_add, ignore_index=True)

"""### Inline report without saving object"""

report = df.profile_report(
    sort=None, html={"style": {"full_width": True}}, progress_bar=False
)
report

"""### Save report to file"""

profile_report = df.profile_report(html={"style": {"full_width": True}})
profile_report.to_file("/tmp/example.html")

"""### More analysis (Unicode) and Print existing ProfileReport object inline"""

profile_report = df.profile_report(
    explorative=True, html={"style": {"full_width": True}}
)
profile_report