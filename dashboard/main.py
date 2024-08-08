import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np
import time
from bd import get_data, login_and_get_token

import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px

def filter_by_date(df, start_date, end_date):
    df['date_incident'] = pd.to_datetime(df['date_incident'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return df[(df['date_incident'] >= start_date) & (df['date_incident'] <= end_date)]

def plot_incidence_types(df):
    incidence_counts = df['type_name'].value_counts()
    colors = px.colors.qualitative.Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=incidence_counts.index,  
            y=incidence_counts.values,  
            marker_color=colors[:len(incidence_counts)]  
        )
    ])
    fig.update_layout(
        title='Distribución de Tipos de Incidencias',
        xaxis_title='Tipo de Incidencia',
        yaxis_title='Cantidad de Incidencias',
        template='plotly_white'
    )

    return fig


def plot_incidence_by_type_and_week(df):
    df['date_incident'] = pd.to_datetime(df['date_incident'])
    df['week'] = df['date_incident'].dt.isocalendar().week
    weekly_incidence = df.groupby(['type_name', 'week']).size().reset_index(name='count')
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly
    for i, type_name in enumerate(weekly_incidence['type_name'].unique()):
        df_type = weekly_incidence[weekly_incidence['type_name'] == type_name]
        fig.add_trace(go.Bar(
            x=df_type['week'],
            y=df_type['count'],
            name=type_name,
            marker=dict(color=colors[i % len(colors)])
        ))
    fig.update_layout(
        title='Número de Incidencias por Tipo y Semana',
        xaxis_title='Semana',
        yaxis_title='Número de Incidencias',
        barmode='stack',
        template='plotly_white'
    )
    return fig


def plot_incidence_time_series(df, time_unit='W'):
    """
    Genera un gráfico de serie temporal para el número de incidencias.
    
    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias.
    time_unit (str): La unidad de tiempo para agrupar los datos. Puede ser 'D' (día), 'W' (semana), 'M' (mes), o 'Y' (año).
    """

    df['date_incident'] = pd.to_datetime(df['date_incident'])

    if time_unit == 'D':
        df['time_period'] = df['date_incident'].dt.date
    elif time_unit == 'W':
        df['time_period'] = df['date_incident'].dt.to_period('W').apply(lambda r: r.start_time)
    elif time_unit == 'M':
        df['time_period'] = df['date_incident'].dt.to_period('M').apply(lambda r: r.start_time)
    elif time_unit == 'Y':
        df['time_period'] = df['date_incident'].dt.to_period('Y').apply(lambda r: r.start_time)
    else:
        raise ValueError("El parámetro 'time_unit' debe ser 'D', 'W', 'M', o 'Y'.")

    time_series_incidence = df.groupby('time_period').size().reset_index(name='count')

    fig = go.Figure(data=[
        go.Scatter(
            x=time_series_incidence['time_period'],  
            y=time_series_incidence['count'],  
            mode='lines+markers',  
            marker=dict(color='skyblue'),
            line=dict(color='blue')
        )
    ])

    fig.update_layout(
        title=f'Número de Incidencias por {time_unit}',
        xaxis_title=f'Período ({time_unit})',
        yaxis_title='Número de Incidencias',
        template='plotly_white',
        xaxis=dict(tickformat='%Y-%m-%d')  
    )

    return fig

def calculate_age(birthdate):
    """Calcula la edad a partir de la fecha de nacimiento."""
    today = datetime.now()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def plot_box_plot_by_incidence_type(df):
    """
    Genera un diagrama de caja para la edad de los ciudadanos agrupada por tipo de incidencia.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias.
    """
    df['citizen_birthdate'] = pd.to_datetime(df['citizen_birthdate'], errors='coerce')

    df['citizen_age'] = df['citizen_birthdate'].apply(calculate_age)
    fig = go.Figure()
    types_of_incidence = df['type_name'].unique()
    colors = px.colors.qualitative.Plotly
    for i, type_name in enumerate(types_of_incidence):
        df_type = df[df['type_name'] == type_name]
        fig.add_trace(go.Box(
            y=df_type['citizen_age'],
            name=type_name,
            marker=dict(color=colors[i % len(colors)])  
        ))
    fig.update_layout(
        title='Distribución de Edades de Ciudadanos por Tipo de Incidencia',
        xaxis_title='Tipo de Incidencia',
        yaxis_title='Edad del Ciudadano',
        template='plotly_white'
    )
    return fig

def find_day_with_most_incidents(df):
    """
    Encuentra el día de la semana con más incidencias.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias.
    
    Retorna:
    str: El día de la semana con más incidencias.
    """
    # Asegurarse de que 'date_incident' esté en formato de fecha
    df['date_incident'] = pd.to_datetime(df['date_incident'], errors='coerce')

    # Extraer el día de la semana (nombre completo)
    df['day_of_week'] = df['date_incident'].dt.day_name()

    # Contar el número de incidencias por día de la semana
    day_counts = df['day_of_week'].value_counts()

    # Encontrar el día de la semana con más incidencias
    most_incidents_day = day_counts.idxmax()
    
    return most_incidents_day, day_counts

def plot_incidence_by_day(df):
    """
    Genera un gráfico de barras para el número de incidencias por día de la semana.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias.
    """
    most_incidents_day, day_counts = find_day_with_most_incidents(df)
    colors = [
        'skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink',
        'lightyellow', 'lightgray'
    ]
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = day_counts.reindex(days_of_week).fillna(0)
    fig = go.Figure()
    for i, day in enumerate(day_counts.index):
        fig.add_trace(go.Bar(
            x=[day],
            y=[day_counts[day]],
            name=day,
            marker=dict(color=colors[i % len(colors)])
        ))
    fig.update_layout(
        title='Número de Incidencias por Día de la Semana',
        xaxis_title='Día de la Semana',
        yaxis_title='Número de Incidencias',
        template='plotly_white'
    )
    return fig

def find_month_with_most_incidents(df):
    """
    Encuentra el mes con más incidencias.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias.
    
    Retorna:
    str: El mes con más incidencias.
    """
    df['date_incident'] = pd.to_datetime(df['date_incident'], errors='coerce')
    df['month'] = df['date_incident'].dt.to_period('M')
    month_counts = df['month'].value_counts().sort_index()
    most_incidents_month = month_counts.idxmax()
    return most_incidents_month, month_counts

def plot_incidence_by_month(df):
    """
    Genera un gráfico de barras para el número de incidencias por mes.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias.
    """
    most_incidents_month, month_counts = find_month_with_most_incidents(df)

    colors = px.colors.qualitative.Plotly

    fig = go.Figure()

    for i, (month, count) in enumerate(month_counts.items()):
        fig.add_trace(go.Bar(
            x=[month.strftime('%Y-%m')],  
            y=[count],
            name=month.strftime('%Y-%m'),
            marker=dict(color=colors[i % len(colors)])
        ))

    fig.update_layout(
        title='Número de Incidencias por Mes',
        xaxis_title='Mes',
        yaxis_title='Número de Incidencias',
        template='plotly_white',
        xaxis_tickangle=-45 
    )
    return fig

def plot_incidence_map(df):
    """
    Genera un mapa detallado que muestra la ubicación de las incidencias usando el estilo open-street-map de Plotly.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias con latitud y longitud.
    """
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='description', 
        color='type_name',  
        title='Ubicación de las Incidencias',
        labels={'latitude': 'Latitud', 'longitude': 'Longitud', 'type_name': 'Tipo de Incidencia'},
        mapbox_style='open-street-map' 
    )
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        template='plotly_white'
    )
    return fig


def plot_incidence_heatmap(df):
    """
    Genera un mapa de calor que muestra la densidad de incidencias usando el estilo open-street-map de Plotly.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias con latitud y longitud.
    """
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    df = df.dropna(subset=['latitude', 'longitude'])
    fig = px.density_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        z=df['type_name'].map(lambda x: 1),  
        radius=10,  
        center={'lat': df['latitude'].mean(), 'lon': df['longitude'].mean()},
        zoom=10,  
        color_continuous_scale='Inferno',  
        mapbox_style='open-street-map',  
        title='Densidad de Incidencias'
    )
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        template='plotly_white'
    )
    return fig


def plot_incidence_heatmap_by_type(df, incidence_type):
    """
    Genera un mapa de calor que muestra la densidad de incidencias del tipo especificado usando el estilo open-street-map de Plotly.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos de incidencias con latitud y longitud.
    incidence_type (str): El tipo de incidencia a filtrar.
    """

    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    df = df.dropna(subset=['latitude', 'longitude'])
    df_filtered = df[df['type_name'] == incidence_type]
    fig = px.density_mapbox(
        df_filtered,
        lat='latitude',
        lon='longitude',
        z=df_filtered['type_name'].map(lambda x: 1),  
        radius=10, 
        center={'lat': df_filtered['latitude'].mean(), 'lon': df_filtered['longitude'].mean()},
        zoom=10, 
        color_continuous_scale='Inferno',  
        mapbox_style='open-street-map',  
        title=f'Densidad de Incidencias: {incidence_type}'
    )

    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        template='plotly_white'
    )

    return fig






st.set_page_config(
    page_title="Segurity AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# App sidebar

with st.sidebar:
    

    st.title("Segurity AI Dashboard 🤖")
    jwt_token = login_and_get_token()
    df = get_data(jwt_token, skip=0, limit=100)
    start_date = st.date_input(
        'Fecha de inicio 📅',
        pd.to_datetime('today') - pd.Timedelta(days=30)
    )
    end_date = st.date_input(
        'Fecha de fin 📆',
        pd.to_datetime('today')
    )
    df_filtered = filter_by_date(df, start_date, end_date)
    




    


# App layout

col = st.columns((4.5, 4.5, 4.5), gap='medium')


with col[0]:

    st.title("Análisis de Tipo de Incidencias 🚨")
    fig_incidence_types = plot_incidence_types(df)
    st.plotly_chart(fig_incidence_types)


    st.title("Análisis de Tipo de Incidencias por semana🚨")
    fig_incidence_by_type_and_week = plot_incidence_by_type_and_week(df)
    st.plotly_chart(fig_incidence_by_type_and_week)

    st.title("Mapa de Calor de Incidencias🚨")
    fig_plot_incidence_heatmap = plot_incidence_heatmap(df)
    st.plotly_chart(fig_plot_incidence_heatmap)

with col[1]:
    st.title("Serie de tiempo de incidencias 🚨")
    time_unit = st.selectbox(
        'Selecciona la unidad de tiempo',
        ['Día', 'Semana', 'Mes', 'Año']
    )
    time_unit_mapping = {'Día': 'D', 'Semana': 'W', 'Mes': 'M', 'Año': 'Y'}
    fig_time_series = plot_incidence_time_series(df, time_unit_mapping[time_unit])
    st.plotly_chart(fig_time_series)

    st.title("Edad de los ciudadanos agrupada por tipo de incidencia🚨")
    fig_box_plot_by_incidence_type = plot_box_plot_by_incidence_type(df)
    st.plotly_chart(fig_box_plot_by_incidence_type)

    st.title("Mapa de incidencias🚨")
    fig_plot_incidence_map = plot_incidence_map(df)
    st.plotly_chart(fig_plot_incidence_map)

with col[2]:
    st.title("Cantidad de Incidencias por día de la semana🚨")
    fig_plot_incidence_by_day = plot_incidence_by_day(df)
    st.plotly_chart(fig_plot_incidence_by_day)

    st.title("Cantidad de Incidencias por mes🚨")
    fig_plot_incidence_by_month = plot_incidence_by_month(df)
    st.plotly_chart(fig_plot_incidence_by_month)

    st.title("Mapa de calor por tipo de inidicencia🚨")
    incidence_types = df['type_name'].unique()  # Obtener todos los tipos de incidencia
    selected_incidence_type = st.selectbox(
        'Selecciona el tipo de incidencia',
        incidence_types
    )
    fig_heatmap = plot_incidence_heatmap_by_type(df, selected_incidence_type)
    st.plotly_chart(fig_heatmap)
