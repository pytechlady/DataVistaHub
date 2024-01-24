import pandas as pd
import plotly.graph_objs as go


class Util:
    
    @staticmethod
    def read_dataset(value):
        df = pd.read_csv(value)
        return df
    
    @staticmethod
    def normalize(df, dc):
        x = df.copy()

        # Check if the specified column y exists before dropping
        
        new_df = x.drop(columns=dc)
  
        for i in new_df:
            x[i] = x[i] / x[i][0]
        print(x.columns)
        return x
    
    @staticmethod
    def interactive_plot(df, x, fig=None):
        if fig is None:
            fig = go.Figure()
        
        copy_df = df.copy()
        
        new_df = copy_df.drop(columns=x)
        # Check if the specified column x exists before dropping
        for i in new_df:
            fig.add_scatter(x=df[x], y=df[i], mode='lines', name=i)

        return fig
    
    @staticmethod
    def daily_return(df, x):
        df_daily_return = df.copy()
        
        new_df = df_daily_return.drop(columns=x)
        # Loop through each stock (while ignoring the x-axis column)
        for i in new_df:
            
            # Loop through each row belonging to the stock
            for j in range(1, len(df)):
                
                # Calculate the percentage of change from the previous day
                df_daily_return.loc[j, i] = ((df.loc[j, i] - df.loc[j-1, i]) / df.loc[j-1, i]) * 100
                
            # set the value of first row to zero since the previous value is not available
            df_daily_return.loc[0, i] = 0

        return df_daily_return
