import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import NearestNeighbors

class IrisDataset:
    
    def __init__(self, 
                 filepath, 
                 rm_dup=False, 
                 rm_null=False, 
                 rm_out=False,
                 scale_mode='standard',
                 to_scale=True):
        self.data = read_from_file(filepath)
        if rm_dup:
            self.data = self.remove_duplicates()
        if rm_null:
            self.data = self.remove_null()
        if rm_out:
            self.data = self.remove_outliers()
        if to_scale:
            self.scaler = StandardScaler() if scale_mode=='standard' else MinMaxScaler()
            self.scaler = self.scaler.fit(self.data[['sepal_length',
                                                     'sepal_width',
                                                     'petal_length',
                                                     'petal_width']])
            self.data.iloc[:, 1:-1] = self.scaler.transform(self.data.iloc[:, 1:-1])
        self.knn_searcher = NearestNeighbors(n_neighbors=10).fit(self.data[['sepal_length',
                                                                            'sepal_width',
                                                                            'petal_length',
                                                                            'petal_width']])
        
    #  Data cleaning functions
    def duplicates_check(self):
        bool_arr = self.data.duplicated(subset=['sepal_length',
                                                'sepal_width',
                                                'petal_length',
                                                'petal_width',
                                                'flower'])
        return any(bool_arr)
    
    def get_duplicates(self):
        duparr = self.data.duplicated(subset=['sepal_length',
                                              'sepal_width',
                                              'petal_length',
                                              'petal_width',
                                              'flower'],
                                      keep=False)
        dup_df = self.data.loc[duparr, :]
        return dup_df
    
    def remove_duplicates(self):
        new_df = self.data.drop_duplicates(subset=['sepal_length',
                                                   'sepal_width',
                                                   'petal_length',
                                                   'petal_width',
                                                   'flower'])
        return new_df
    
    def null_check(self):
        return self.data.isnull().to_numpy().any()
    
    def get_null(self):
        nullarr = self.data.isnull().any(axis=1)
        new_df = self.data.loc[nullarr,:]
        return new_df
    
    def remove_null(self):
        new_df = self.data.dropna()
        return new_df
    
    def check_outliers(self, v):
        var_col = self.data[v]
        q1 = var_col.quantile(q=0.25)
        q3 = var_col.quantile(q=0.75)
        iqr = q3 - q1
        bool_arr = ~var_col.between(q1-(1.5*iqr), q3+(1.5*iqr))
        return bool_arr.any()
    
    def get_outliers(self, v):
        var_col = self.data[v]
        q1 = var_col.quantile(q=0.25)
        q3 = var_col.quantile(q=0.75)
        iqr = q3 - q1
        bool_arr = ~var_col.between(q1-(1.5*iqr), q3+(1.5*iqr))
        outlier_df = self.data.loc[bool_arr, :]
        return outlier_df
    
    def get_flower_outliers(self, flwr, v):
        flwr_data = self.data.loc[self.data['flower']==flwr, :]
        var_col = flwr_data.loc[:, v]
        q1 = var_col.quantile(q=0.25)
        q3 = var_col.quantile(q=0.75)
        iqr = q3 - q1
        bool_arr = (~var_col.between(q1-(1.5*iqr), q3+(1.5*iqr))).to_numpy()
        outlier_df = flwr_data.loc[bool_arr, :]
        return outlier_df
    
    def remove_outliers(self):
        out_arr = np.full(shape=(1,len(self.data)), fill_value=False)
        for v in self.data.columns[1:-1]:
            if self.check_outliers(v):
                var_col = self.data[v]
                q1 = var_col.quantile(q=0.25)
                q3 = var_col.quantile(q=0.75)
                iqr = q3 - q1
                out_arr = np.append(out_arr, 
                                    np.expand_dims(var_col.between(q1-(1.5*iqr), 
                                                                   q3+(1.5*iqr)).to_numpy(), 
                                                   axis=0), 
                                    axis=0)
        out_arr = out_arr.any(axis=0)
        new_df = self.data.loc[out_arr, :]
        return new_df
    
    # Data visualisation functions
    
    def plot_overall_boxplot(self, for_tk=False):
        fig, ax = plt.subplots(figsize=(6,4))
        sns.boxplot(data=self.data.iloc[:, 1:], ax=ax).set(ylabel="Values (cm)", 
                                                           xlabel="Measurements",
                                                           title="Boxplot for overall data distribution")
        if for_tk:
            return fig
        else:
            return ax
        
    def plot_overall_vplot(self, for_tk=False):
        fig, ax = plt.subplots(figsize=(6,4))
        sns.violinplot(data=self.data.iloc[:, 1:], ax=ax).set(ylabel="Values (cm)",
                                                              xlabel="Variable",
                                                              title="Violin plot for overall data distribution")
        if for_tk:
            return fig
        else:
            return ax
        
    def plot_stratified_boxplot(self, for_tk=False):
        fig, ax = plt.subplots(figsize=(6,4))
        tmp = pd.melt(self.data, id_vars='flower', 
                      value_vars=["sepal_length",
                                  "sepal_width",
                                  "petal_length",
                                  "petal_width"])
        sns.boxplot(x='variable', 
                    y='value', 
                    hue='flower', 
                    palette=["r", "b", "g"],
                    data=tmp,
                    ax=ax).set(xlabel="Variable", 
                               ylabel="Values (cm)",
                               title="Boxplot for stratified data distribution")
        sns.move_legend(ax, "upper right", title=None)
        if for_tk:
            return fig
        else:
            return ax
    
    def plot_stratified_vplot(self, for_tk=False):
        fig, ax = plt.subplots(figsize=(6,4))
        tmp = pd.melt(self.data, id_vars='flower', 
                      value_vars=["sepal_length",
                                  "sepal_width",
                                  "petal_length",
                                  "petal_width"])
        sns.violinplot(x='variable', 
                       y='value', 
                       hue='flower', 
                       palette=["r", "b", "g"],
                       data=tmp,
                       ax=ax).set(xlabel="Variable", 
                                  ylabel="Values (cm)",
                                  title="Violin plot for stratified data distribution")
        sns.move_legend(ax, "upper right", title=None)
        if for_tk:
            return fig
        else:
            return ax
    
    # Generate neighbors using k-NN
    
    def get_knn(self, obs):
        tmp_df = pd.DataFrame([obs])
        tmp_df.iloc[:,:] = self.scaler.transform(tmp_df)
        distances, idxs = self.knn_searcher.kneighbors(tmp_df, n_neighbors=10)
        nb_data = self.data.iloc[idxs[0],:].copy()
        nb_data.iloc[:, 1:-1] = self.scaler.inverse_transform(nb_data.iloc[:, 1:-1])
        nb_data.insert(5, 'distance', distances[0])
        return nb_data.sort_values(by='distance', axis=0, ascending=False)
    
    
    def plot_neighbors(self, obs, for_tk=False):
        nb_df = self.get_knn(obs)
        fig, ax = plt.subplots(figsize=(6,4))
        tmp = pd.melt(nb_df, 
                      id_vars=['flower', 'distance'],
                      value_vars=['sepal_length',
                                  'sepal_width',
                                  'petal_length',
                                  'petal_width'])
        sns.swarmplot(x='variable',
                      y='value',
                      hue='flower',
                      ax=ax,
                      alpha=0.7,
                      data=tmp).set(xlabel='Variable',
                                    ylabel='Values (cm)',
                                    title="Data distribution of 10 most similar observations")
        for x, y in obs.items():
            ax.scatter(x, y, color='r', marker='x')
        if for_tk:
            return fig
        else:
            return ax
        
    
            
def read_from_file(fp):
    data = pd.read_csv(fp,
                       header=None,
                       index_col=False,
                       names=['sepal_length',
                              'sepal_width',
                              'petal_length',
                              'petal_width',
                              'flower'])
    data.insert(0, 'id', data.index)
    return data
