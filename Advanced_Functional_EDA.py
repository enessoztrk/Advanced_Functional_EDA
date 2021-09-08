#############################################
# ADVANCED FUNCTIONAL EXPLORABLE DATA ANALYSIS
#############################################

# Read across persona.csv and show your general information with the dataset.
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

df = pd.read_csv(r'C:\Users\hp\Masaüstü\VBO\Week.02\Notes\persona.csv')
df.head()
df.info()
df.shape

# How many unique SOURCE are there? What are their frequencies?
df["SOURCE"].nunique()
len(set(df["SOURCE"]))
df["SOURCE"].value_counts()

# How many unique PRICEs are there?
df["PRICE"].nunique()

# How many of which PRICE have been realized?
df["PRICE"].value_counts()

# How many sales from which country?
df["COUNTRY"].value_counts()

# How much was earned in total from sales by country?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})

# What are the sales numbers according to SOURCE types?
df["SOURCE"].value_counts()
df.groupby("SOURCE")["PRICE"].count()
df.groupby("SOURCE").agg({"PRICE": "count"})
# 3 different uses

# What are the PRICE averages by country?
df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"})

# What is the average PRICE by country and sex?
df.groupby(['COUNTRY','SEX']).agg({"PRICE": "mean"})

# What are the PRICE averages according to SOURCE?
df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})
df.groupby(['SOURCE']).agg({"PRICE": "mean"})

# What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(['COUNTRY','SOURCE']).agg({"PRICE":"mean"})
df.groupby(by=["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

# What are the total gains broken down by COUNTRY, SOURCE, SEX, AGE?
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"sum"})
df.groupby(by=["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "sum"})

# Sort the above output according to PRICE.
agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "sum"}).sort_values("PRICE", ascending=False)
agg_df.head()
agg_df.sort_values(by="PRICE", ascending=False)

# All impressions indexes in PRICE in the above place are output.
# We should try to convert these names to variable names. To return to our initial data.
agg_df = agg_df.reset_index()
agg_df.head()

# Convert AGE variable to categorical variable and add it to agg_df.
# Convert the numeric variable age to a categorical variable.
# Construct the intervals as you think will be persuasive.
# For example: '0_18', '19_23', '24_30', '31_40', '41_70'

# Let's specify from where the AGE variable will be divided:
bins = [0, 19, 24, 31, 41, agg_df["AGE"].max()]

# What the nomenclature means for the dividing points:
mylabels = ['0_18', '19_24', '24_30', '30_40', '40_' + str(agg_df["AGE"].max())]

# Let's divide AGE:
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

# Define new level based customers and add them as variables to the dataset.

# A variable named customers_level_based should be defined and added to the dataset.
# Attention!
# After the values are created, these values need to be deduplicated.
# For example, more than one of the following expressions: USA_ANDROID_MALE_0_18
# It is necessary to take them to groupby and get the price average.

# Variable Names:
agg_df.columns

# How do we access the observation values?
for dff in agg_df.values:
    print(dff)

# We want to put the VALUES of the COUNTRY, SOURCE, SEX and age_cat variables side by side and concatenate them with an underscore.
# We can do this with list comprehension.

# Let's perform the operation in such a way that we select the observation values in the above loop:
[dff[0].upper() + "_" + dff[1].upper() + "_" + dff[2].upper() + "_" + dff[5].upper() for dff in agg_df.values]

# Let's add it to the dataset:
agg_df["customers_level_based"] = [dff[0].upper() + "_" + dff[1].upper() + "_" + dff[2].upper() + "_" + dff[5].upper() for dff in agg_df.values]
agg_df.head()

# Let's remove the unnecessary variables:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

# Check:
agg_df["customers_level_based"].value_counts()

# After groupby according to the segments, we need to get the price averages and deduplicate the segments.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.head()

# It is in the customers_level_based index.
agg_df = agg_df.reset_index()
agg_df.head()

# Check. Each persona is expected to have one:
agg_df["customers_level_based"].value_counts()
agg_df.head()

# Segment new customers (USA_ANDROID_MALE_0_18).
###########################################
# New customers (Example: USA_ANDROID_MALE_0_18)
# SEGMENT by PRICE,
# add segments to agg_df with the naming "SEGMENT",
# describe the SEGMENT,
# Analyze the C SEGMENT.

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})
agg_df[agg_df["SEGMENT"] == "C"]
agg_df[agg_df["SEGMENT"] == "D"]["PRICE"].describe().T
agg_df[agg_df["SEGMENT"] == "C"]["PRICE"].describe().T
agg_df[agg_df["SEGMENT"] == "B"]["PRICE"].describe().T
agg_df[agg_df["SEGMENT"] == "A"]["PRICE"].describe().T

# Classify the new customers and estimate how much income they can bring.
#############################################

# What segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# In which segment and how much income on average would a 35-year-old French woman using iOS expect to earn?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

#A,B,C,D