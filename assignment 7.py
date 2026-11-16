
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tkinter import Tk, filedialog

# ==========================================
# 1. LOAD DATASET
# ==========================================

def load_dataset():

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Dataset",
        filetypes=[
            ("Dataset Files", "*.csv *.xls *.xlsx")
        ]
    )

    if not file_path:
        print("No file selected!")
        return None

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(file_path)

    elif extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)

    else:
        print("Unsupported file format!")
        return None

    print("\nDataset Loaded Successfully!")
    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nDataset Information:")
    df.info()

    print("\nDataset Description:")
    print(df.describe(include="all"))

    return df, file_path


# ==========================================
# 2. BASIC DATA PREPROCESSING
# ==========================================

def preprocess_data(df):

    df = df.copy()

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing values
    for col in df.columns:

        if df[col].isnull().any():

            if pd.api.types.is_numeric_dtype(df[col]):

                df[col] = df[col].fillna(
                    df[col].median()
                )

            else:

                mode = df[col].mode()

                if not mode.empty:
                    df[col] = df[col].fillna(mode.iloc[0])
                else:
                    df[col] = df[col].fillna("Unknown")

    print("\nData Preprocessing Completed!")

    return df


# ==========================================
# 3. IDENTIFY COLUMN TYPES
# ==========================================

def identify_columns(df):

    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    print("\nNumerical Columns:", numerical_columns)
    print("Categorical Columns:", categorical_columns)

    return numerical_columns, categorical_columns


# ==========================================
# 4. LINE PLOT
# ==========================================

def line_plot(df, numerical_columns):

    if len(numerical_columns) == 0:
        print("No numerical columns for line plot.")
        return

    plt.figure(figsize=(10, 5))

    for col in numerical_columns[:5]:
        plt.plot(
            df.index,
            df[col],
            marker="o",
            label=col
        )

    plt.title("Line Plot")
    plt.xlabel("Data Index")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ==========================================
# 5. BAR PLOT
# ==========================================

def bar_plot(df, numerical_columns):

    if len(numerical_columns) == 0:
        print("No numerical columns for bar plot.")
        return

    column = numerical_columns[0]

    plt.figure(figsize=(10, 5))

    df[column].head(20).plot(
        kind="bar",
        color="skyblue"
    )

    plt.title("Bar Plot - " + column)
    plt.xlabel("Data Index")
    plt.ylabel(column)
    plt.tight_layout()
    plt.show()


# ==========================================
# 6. SCATTER PLOT
# ==========================================

def scatter_plot(df, numerical_columns):

    if len(numerical_columns) < 2:
        print("At least 2 numerical columns required.")
        return

    plt.figure(figsize=(8, 5))

    sns.scatterplot(
        data=df,
        x=numerical_columns[0],
        y=numerical_columns[1],
        color="red"
    )

    plt.title("Scatter Plot")
    plt.xlabel(numerical_columns[0])
    plt.ylabel(numerical_columns[1])
    plt.tight_layout()
    plt.show()


# ==========================================
# 7. HEATMAP
# ==========================================

def heatmap(df, numerical_columns):

    if len(numerical_columns) < 2:
        print("At least 2 numerical columns required.")
        return

    correlation = df[numerical_columns].corr()

    plt.figure(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )

    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()


# ==========================================
# 8. HISTOGRAM
# ==========================================

def histogram(df, numerical_columns):

    if len(numerical_columns) == 0:
        return

    df[numerical_columns].hist(
        figsize=(12, 8),
        bins=20,
        color="orange",
        edgecolor="black"
    )

    plt.suptitle("Histogram of Numerical Features")
    plt.tight_layout()
    plt.show()


# ==========================================
# 9. BOX PLOT
# ==========================================

def box_plot(df, numerical_columns):

    if len(numerical_columns) == 0:
        return

    plt.figure(figsize=(10, 6))

    sns.boxplot(
        data=df[numerical_columns]
    )

    plt.title("Box Plot")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ==========================================
# 10. PAIR PLOT
# ==========================================

def pair_plot(df, numerical_columns):

    if len(numerical_columns) < 2:
        return

    selected_columns = numerical_columns[:5]

    sns.pairplot(
        df[selected_columns],
        diag_kind="hist"
    )

    plt.suptitle(
        "Pair Plot",
        y=1.02
    )

    plt.show()


# ==========================================
# 11. SAVE PREPROCESSED DATA
# ==========================================

def save_dataset(df, file_path):

    output_path = (
        os.path.splitext(file_path)[0]
        + "_preprocessed.csv"
    )

    df.to_csv(output_path, index=False)

    print("\nPreprocessed Dataset Saved:")
    print(output_path)


# ==========================================
# 12. MAIN FUNCTION
# ==========================================

def main():

    print("======================================")
    print(" DATA PREPROCESSING AND VISUALIZATION")
    print("======================================")

    result = load_dataset()

    if result is None:
        return

    df, file_path = result

    # Preprocessing
    df = preprocess_data(df)

    # Identify columns
    numerical_columns, categorical_columns = (
        identify_columns(df)
    )

    # Generate plots
    print("\nGenerating Visualizations...")

    line_plot(df, numerical_columns)

    bar_plot(df, numerical_columns)

    scatter_plot(df, numerical_columns)

    heatmap(df, numerical_columns)

    histogram(df, numerical_columns)

    box_plot(df, numerical_columns)

    pair_plot(df, numerical_columns)

    # Save dataset
    save_dataset(df, file_path)

    print("\nAll Operations Completed Successfully!")


if __name__ == "__main__":
    main()
