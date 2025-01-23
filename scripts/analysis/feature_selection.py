import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from salmonella_study.config import Config

from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold

processed_data_path = Config.PROCESSED_DATA_DIR

# Load merged dataset
merged_data_path = os.path.join(processed_data_path, "salmonella_population", "sense-d_socioecono_salmonella_MO_2020.csv")
df = pd.read_csv(merged_data_path)

# Remove columns with a lot of missing values
missing_threshold = 0.3  # Example: remove columns with more than 30% missing values
df = df.loc[:, df.isnull().mean() < missing_threshold]

# Remove low variance columns
variance_threshold = 0.01  # Example: remove columns with variance below 0.01
selector = VarianceThreshold(threshold=variance_threshold)
df = df.loc[:, selector.fit(df).get_support()]

# Apply PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(df.select_dtypes(include=[np.number]))  # Assuming you want to use only numeric columns

# Create a DataFrame for the principal components
pc_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Get explained variance
explained_variance = pca.explained_variance_ratio_

# Print results
print("Principal Components:\n", pc_df)
print("Explained Variance Ratio:", explained_variance)

