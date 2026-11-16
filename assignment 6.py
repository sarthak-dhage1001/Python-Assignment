
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tkinter import Tk, filedialog


# ==========================================
# 1. SELECT INPUT FILE
# ==========================================

def select_file():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select CSV or Excel File",
        filetypes=[
            ("Data Files", "*.csv *.xls *.xlsx"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xls *.xlsx")
        ]
    )

    return file_path


# ==========================================
# 2. LOAD DATASET
# ==========================================

def load_data(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(file_path)

    elif extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format!")

    print("\nOriginal Dataset:")
    print(df.head())

    return df


# ==========================================
# 3. DATA PREPROCESSING
# ==========================================

def preprocess_data(df):

    print("\nStarting Data Preprocessing...")

    # Make a copy
    df = df.copy()

    # --------------------------------------
    # A. CLEAN COLUMN NAMES
    # --------------------------------------

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------
    # B. REMOVE DUPLICATES
    # --------------------------------------

    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()

    print("Duplicates removed:", duplicate_count)

    # --------------------------------------
    # C. HANDLE MISSING VALUES
    # --------------------------------------

    for column in df.columns:

        if df[column].isnull().sum() > 0:

            if pd.api.types.is_numeric_dtype(df[column]):

                df[column] = df[column].fillna(
                    df[column].median()
                )

            else:

                mode_value = df[column].mode()

                if not mode_value.empty:
                    df[column] = df[column].fillna(
                        mode_value.iloc[0]
                    )
                else:
                    df[column] = df[column].fillna("Unknown")

    print("Missing values handled.")

    # --------------------------------------
    # D. CONVERT DATA TYPES
    # --------------------------------------

    for column in df.columns:

        if df[column].dtype == "object":

            converted = pd.to_numeric(
                df[column], errors="coerce"
            )

            # Convert only if most non-null values are numeric
            if converted.notna().sum() > 0:
                if converted.notna().sum() / max(
                    df[column].notna().sum(), 1
                ) >= 0.8:

                    df[column] = converted.fillna(
                        converted.median()
                    )

    print("Data types checked.")

    # --------------------------------------
    # E. HANDLE OUTLIERS USING IQR
    # --------------------------------------

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        df[column] = df[column].clip(
            lower_limit, upper_limit
        )

    print("Outliers handled using IQR.")

    # --------------------------------------
    # F. ENCODE CATEGORICAL VARIABLES
    # --------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns

    for column in categorical_columns:

        encoder = LabelEncoder()

        df[column] = encoder.fit_transform(
            df[column].astype(str)
        )

    print("Categorical variables encoded.")

    # --------------------------------------
    # G. NORMALIZE NUMERICAL FEATURES
    # --------------------------------------

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    if len(numeric_columns) > 0:

        scaler = StandardScaler()

        df[numeric_columns] = scaler.fit_transform(
            df[numeric_columns]
        )

    print("Numerical features standardized.")

    return df


# ==========================================
# 4. SAVE CLEANED DATASET
# ==========================================

def save_data(df, input_path):

    output_path = os.path.splitext(
        input_path
    )[0] + "_preprocessed.csv"

    df.to_csv(output_path, index=False)

    print("\nPreprocessed dataset saved successfully!")
    print("Output File:", output_path)


# ==========================================
# 5. MAIN FUNCTION
# ==========================================

def main():

    print("====================================")
    print("     AUTOMATIC DATA PREPROCESSING")
    print("====================================")

    file_path = select_file()

    if not file_path:
        print("No file selected!")
        return

    try:

        # Load dataset
        df = load_data(file_path)

        # Display dataset information
        print("\nDataset Information:")
        print(df.info())

        print("\nMissing Values:")
        print(df.isnull().sum())

        # Preprocess dataset
        cleaned_df = preprocess_data(df)

        # Display cleaned dataset
        print("\nCleaned Dataset:")
        print(cleaned_df.head())

        print("\nFinal Dataset Shape:", cleaned_df.shape)

        # Save output
        save_data(cleaned_df, file_path)

    except Exception as e:

        print("\nError occurred:", e)


if __name__ == "__main__":
    main()
