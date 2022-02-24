import numpy as np
import pandas as pd

'''
SERIES:
Pandas Series is a one-dimensional labeled array capable of holding data of any type (integer, string, float, python objects, etc.). 
The axis labels are collectively called index. 
Pandas Series is nothing but a column in an excel sheet.

'''
numbers = [1, 2, 3, 4, 5]
ser = pd.Series(numbers)
# print(ser)

'''
DATAFRAME:
Two-dimensional size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns).
Arithmetic operations align on both row and column labels. 
Can be thought of as a dict-like container for Series objects. The primary pandas data structure.

'''
sales_df = pd.read_csv("/home/prashanth/Documents/docs/1000 Sales Records.csv")
sales_df = sales_df.set_index("Country")
# print(sales_df.tail())

# todo Reading Headers
print(sales_df.columns)

# todo specific column

# print(sales_df.Region)
# print(sales_df[["Region","Total Cost"]])
# todo read each column

# print(sales_df.iloc[1:4])

# todo Read a Specific LOcation

# print(sales_df.iloc[2,4])
# for index, row in sales_df.iterrows():
#     print(index,row["Total Cost"])


# print(sales_df.loc[sales_df["Region"]=="Europe"])
# todo describe table

# print(sales_df.describe())

# todo sorting

# print(sales_df.sort_values(["Sales Channel","Region","Total Cost"],ascending=False).iloc[0]["Total Profit"])

# print(sales_df.sort_values(["Item Type","Unit Cost"],ascending=[1,0]).iloc[0].Region)


# TODO MAKING CHANGES IN DATA

# todo adding columnns data

Costdf = sales_df["Total Unit Price"] = sales_df["Unit Cost"] + sales_df["Total Cost"]
# print(sales_df["Total Unit Price"])
sales_df["Total"] = sales_df.iloc[:, 9:11].sum(axis=1)
# print(sales_df[['Unit Price', 'Unit Cost','Total']])
# print(sales_df.iloc[:,9:])

# todo drop column

# print(sales_df.drop(columns=["Ship Date"]))
# todo rearranging columns

# sales_df = sales_df[["Item Type","Order Date","Total Cost"]]
# print(sales_df.head(5))
# cols = sales_df.columns.values
cols = list(sales_df.columns)
# print(sales_df[cols[9]])


# TODO FILTERING DATA


# print(sales_df[(sales_df["Region"]=="Europe") & (sales_df["Item Type"]=="Clothes")])
sales_f_data = sales_df[
    (sales_df["Region"] == "Europe") & (sales_df["Item Type"] == "Clothes") | (sales_df["Total"] > 100)]
sales_f_data.reset_index(drop=True, inplace=True)  # modified or Setup the New index From First Onwars

# todo Filtering the data which containd the specific string content

# print(sales_f_data.loc[sales_f_data["Region"].str.contains("st")])
# print(sales_f_data.loc[~sales_f_data["Region"].str.contains("rope")])

import re

# todo Using Regex

# print(sales_f_data.loc[sales_f_data["Region"].str.contains("rope|st",regex = True)])
# print(sales_f_data.loc[sales_f_data["Region"].str.contains("Rope|St",flags = re.I,regex = True)]) # ignore CaseSensitive

print(sales_df.loc[sales_df["Item Type"].str.contains('^C[a-z]', flags=re.I, regex=True)])

# TODO CONDITIONAL STATEMENT  CHANGES:

sales_f_data.loc[sales_f_data["Region"] == "Europe", "Region"] = "Europian Countries"
# print(sales_f_data)

# CHange Multiple Columns At a Time

sales_df.loc[sales_df['Total'] > 1200, ["Item Type", "Total Revenue"]] = ["LE1200", "Cost_low1200"]
# print(sales_df[["Item Type","Total Revenue"]])

# TODO AGGRGATE STATISTICS

# print(sales_df.groupby(["Total"]).mean().sort_values("Total",ascending=True))
print(sales_df.groupby(["Total Revenue", "Item Type"]).count())
print(sales_df.groupby("Total Revenue").mean())

# TODO MAPPING ,APPLY,APPLYMAP

# Todo TERMINOLOGY ALERT

'''
MAP : Gives the mapping between column values

    Ex: df["new_feature] = df.column.map({"key":1,"key1":2)
'''
# print(sales_df.Region.map())
# todo check dataset having null values or not
print(sales_df.isna().sum())

# todo multi_indexing
# print(sales_df.set_index(["Region","Item Type"],inplace=True))  # creating multiple indexes
# print(sales_df.sort_index(inplace=True))
# print(sales_df)

# todo filtering data from multiindex df
print(sales_df.loc[
      ("Asia", "Canada"), :
      ])
# todo for getting total multiindex columns with data
# use to pass the slice(None)


# ToDO PAnDAs TricKs :

1  # Show installe versions:
print(pd.__version__)
# print(pd.show_versions()) #dependencies

2  # Create Example DataFrame

pdf = pd.DataFrame({"col_1": [12, 4124, 42344], "col2": [234, 242, 423]})
# print(pdf)

# print(pd.DataFrame(np.random.rand(9923,4234),columns=list(range(4234))))

3.  # Rename Columns
sales_df.rename({"OldCol_1": "NewCol_1", "OldCol_2": "NewCol_2"})
sales_df.columns = ["OldCol", "NewCol"]
sales_df.columns = sales_df.columns.str.replace(" ", "_")
# for addding of Prefix& Suffix to columns

sales_df.add_prefix("PDs")
sales_df.add_suffix("Dfm")

4.  # Reverse Row_ORder
sales_df.loc[::-1].head()  # index order willl changes
sales_df.loc[::-1].reset_index(drop=True).head()  # index order will be in the order

5.  # Reverse ColumnOrder
sales_df.loc[:, ::-1].head()

6.  # Select Columns By the Datatypes

sales_df.select_dtypes(include="number").head()  # Gives the Both int And Float Columns
sales_df.select_dtypes(include="object")  # Only Objects
sales_df.select_dtypes(include=["Object", "number", "category", "datetime"])
sales_df.select_dtypes(exclude="number")

7.  # Convert sting to Numbers

sales_df.astype({"col_!": float, "col_2": float})
pd.to_numeric(sales_df.col1, errors="fef").fillna(0)

8.  # Reduce DataFrame Size
sales_df.info()  # tells about the Size
cols = ["col1", "col2"]
dtypes = {"column": "category"}
sales_df = pd.read_csv("path", usecols=cols, dtype=dtypes)

9  # Build a DataFramre By Multiple-Files (Row-Size)

import glob

files_list = sorted(glob("file_name*.csv"))
dataframe = pd.concat((pd.DataFrame(csv) for csv in files_list), ignore_index=True)

10  # Build a DataFramre By Multiple-Files (Column-Size)

import glob

files_list = sorted(glob("file_name*.csv"))
dataframe = pd.concat((pd.DataFrame(csv) for csv in files_list), axis="columns")

11  # Create Dataframe From Clipboard

dafr = pd.read_clipboard()  # copy from any excel sheets and execute the reader function

12.  # Split DataFrame Into Two RandomSubsets

# we have the dataframe having some large amount of the length

data_frame = pd.DataFrame(np.random.rand(1000, 50))
data_frame1 = data_frame.sample(frac=0.57, random_state=1234)
data_frame2 = data_frame.drop(data_frame1.index)
# want ot see indexes of the two dataframes
data_frame1.index.sort_values()

13  # Filter the DataFrame By Multiple Categories

sales_df.Total.unique()
sales_df[("Col1" == "val") | ("Col2" == "val2") | ("col3" == "val4")].head()
sales_df[~sales_df.isin(["col1", "col2"])]

14.  # Filter a Dataframe by the Largest Category values

counts = sales_df.TOtal.value_counts()
counts.nlargest(3)

15.  # Handle Missing Values
sales_df.isna().sum()
# drop column of missing columns
sales_df.dropna(axis="columnns")

# We Can Threshold For Dropna
sales_df.dropna(thresh=len(sales_df) * 0.9, axis="columnns")

16.  # Split a String Into Multiple Columns

DatFr = pd.DataFrame({"name": ["Arun Vijay prashanth", "manoj venkat,manohar"], "palce": ["tap", "miwe"]})
DatFr = DatFr.name.str.split(" ", expand=True)

17.  # Expands a Series Of Lists Into a DataFrame
import pandas as pd

DF = pd.DataFrame({"name": ["Raees", "rear", "etr"], "range": [[12, 2], [312, 44], [2424, 2343]]})
DF_new = DF.range.apply(pd.Series)

df = pd.concat([DF, DF_new], axis="columns")

18.  # Aggregate By Multiple Functions

sales_df.groupby("Item Type").Total.sum()
sales_df.groupby("Item Type").Total.agg(["sum", "count"])

19.  # Combine the Output Of an Aggregation With DataFrame

Total_Sum = sales_df.groupby("Item Type").Total.transform(
    "sum")  # performs same as the sum() function but treturns he output will be in the same shape of the InputData
df["Total_Sum"] = Total_Sum

20.  # Select the Slice Of Rows & Columns

sales_df.describe().loc["min":"max", "col1":"col2"]

21  # Reshaped A MultiindexedSeries

sales_df.groupby("Item Type").Total.mean().unstack()

# Todo Terminology Alert

'''
Usage of "unstack":-- To Reshape a Multiindeable Series into a DataFraame

'''

22  # Create a PivotTable

# More Convinient to Change the original Data Frame
sales_df.pivot_table(index="Region", columns="Total Revenue", values="values_column", aggfunc="mean",
                     margins=True)  # margin =True --> overal Rate reg(columns,rows)

23.  # Convert ContinuousData into Categorical Data

pd.cut(sales_df.Total, bins=[0, 240, 2344], labels=["low", "medium", "high"])

24  # Change Dispaly options

pd.set_option("display.float_format", "{:.2f}".format())
# wecan also any option to reset the default
pd.reset_option("display.float_format")

25.  # Style a DataFrame

# here we should prepare a format dict According to our Requirement

format_dict = {"col_1": "{:%m,%y,%d}", "col2": "${:.2f}"}
sales_df.style.format(format_dict)

# todo Profile a DataFrame
import pandas_profiling

pandas_profiling.profileReport(sales_df)

# todo Count the Null Columns

train = pd.read_csv("train.csv")
null_columns = train.columns[train.isnull().any()]
train[null_columns].isnull().sum()

# todo Single Column Is Null


print(train[train["Electrical"].isnull()][null_columns])

# todo All Null Columns
print(train[train.isnull().any(axis=1)][null_columns].head())
