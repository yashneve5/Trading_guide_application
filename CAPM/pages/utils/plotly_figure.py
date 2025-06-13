import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime
from plotly.graph_objects import Table, Figure

def plotly_table(dataframe):
    import plotly.graph_objects as go

    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + ["<b>" + str(i)[:10] + "</b>" for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[
                ["<b>" + str(i) + "</b>" for i in dataframe.index]
            ] + [
                ["<b>" + str(val) + "</b>" for val in dataframe[col]] for col in dataframe.columns
            ],
            fill_color=[[rowOddColor, rowEvenColor] * (len(dataframe) // 2 + 1)],
            align='left',
            line_color='white',
            font=dict(color="black", size=15)
        )
    )])

    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig
def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '3d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '1w':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(weeks=-1)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]
    
    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close']
    ))
    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#efefff',
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )
    return fig

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(width=2, color='#007fff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(width=2, color='red')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#efefff',
        legend=dict(yanchor="top", xanchor="right"),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )
    return fig

def RSI(dataframe, num_period):
    dataframe = dataframe.copy()
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['RSI'].tolist(), name='RSI', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe), name='Overbought', line=dict(width=2, color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), fill='tonexty', name='Oversold', line=dict(width=2, color='#79da84', dash='dash')))
    fig.update_layout(
        yaxis_range=[0, 100],
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#efefff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )
    return fig

def Moving_average(dataframe, num_period):
    dataframe = dataframe.copy()
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(width=2, color='#007fff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(width=2, color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'], mode='lines', name='SMA 50', line=dict(width=2, color='purple')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#efefff',
        legend=dict(yanchor="top", xanchor="right"),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )
    return fig

def Moving_average_candle_stick(dataframe, num_period):
    dataframe = dataframe.copy()
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close'],
        name='Candlestick'
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['SMA_50'],
        mode='lines',
        name='SMA 50',
        line=dict(width=2, color='purple')
    ))
    fig.update_layout(
        showlegend=True,
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#efefff',
        xaxis_rangeslider_visible=False,
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )
    return fig

def MACD(dataframe, num_period):
    dataframe = dataframe.copy()
    macd_df = pta.macd(dataframe['Close'])
    dataframe['MACD'] = macd_df.iloc[:, 0]
    dataframe['MACD_Signal'] = macd_df.iloc[:, 1]
    dataframe['MACD_Hist'] = macd_df.iloc[:, 2]
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'].tolist(), name='MACD', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD_Signal'].tolist(), name='Signal', line=dict(width=2, color='red', dash='dash')))
    fig.update_layout(
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#efefff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )
    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast.index[:-30],
        y=forecast['Close'].iloc[:-30],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='black')
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index[-31:],
        y=forecast['Close'].iloc[-31:],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(yanchor="top", xanchor="right")
    )
    return fig
