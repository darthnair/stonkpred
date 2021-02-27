import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


START = "2013-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Predict your stocks -")

stonk = ("AAPL", "DOGE-USD", "ETH-USD", "MRNA", "PYPL", "GM")
selectstonk = st.selectbox("Choose stock for prediction", stonk)

nyears = st.slider("No. of years for prediction:", 1, 5)
period = nyears*365

@st.cache
def load_stock(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Loading stonk...")
data = load_stock(selectstonk)
data_load_state.text("Done")

st.subheader('Raw Data')
st.write(data.tail())


def plotraw():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock Opening'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Opening'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plotraw()



df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

x = Prophet()
x.fit(df_train)
future = x.make_future_dataframe(periods=period)
forecast = x.predict(future)

st.subheader('Forecast stonk')
st.write(forecast.tail())

st.write('Forecast stonk')
fig2 = plot_plotly(x, forecast)
st.plotly_chart(fig2)

st.write('forecast components')
fig3 = x.plot_components(forecast)
st.write(fig3)
