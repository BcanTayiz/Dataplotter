import streamlit as st
import pandas as pd
import numpy as np
import googletrans
from googletrans import Translator
import seaborn as sns
from matplotlib import pyplot
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from googletrans import Translator
import os
import base64
import xlsxwriter
from io import StringIO
import cgi
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
import os

import sys
def my_except_hook(exctype, value, traceback):
        print('The translation is not done, please refresh the page or retry the program function')
sys.excepthook = my_except_hook


port = int(os.environ.get(“PORT”, 5000))


st.title("Plot your Data")
st.header("Load your data & plot it")


st.set_option('deprecation.showPyplotGlobalUse', False)


data = pd.read_csv('data_tr.csv')

sns.set(rc={'figure.figsize':(15,8.27)})




STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

FILE_TYPES = ["csv","xlsx"]

translator = Translator()

st.title("")

class FileType(Enum):
    """Used to distinguish between file types"""

    IMAGE = "Image"
    CSV = "csv"
    PYTHON = "Python"
    EXCEL = "Excel"

def plotData(data,x,y,z):
    if (is_string_dtype(data[x]) and is_numeric_dtype(data[y])) or (is_numeric_dtype(data[x]) and is_string_dtype(data[y])):
        try:
            g = sns.barplot(x=x, y=y,hue=z, data=data)
        except:
            pass
        if (is_string_dtype(data[x]) and is_numeric_dtype(data[y])):
            g.set_yticklabels(g.get_yticklabels(),rotation=60)
        else:
            g.set_xticklabels(g.get_xticklabels(),rotation=60)
        st.pyplot()
    elif (is_numeric_dtype(data[x]) and is_numeric_dtype(data[y])):
        try:
            g = sns.scatterplot( x=x, y=y,hue=z, data=data)
        except:
            pass
        st.pyplot()
    elif (is_string_dtype(data[x]) and is_string_dtype(data[y])):
        g_1 = sns.countplot(x=x,data=data)
        g_1.set_xticklabels(g_1.get_xticklabels(),rotation=60)
        st.pyplot()

        g_2 = sns.countplot(x=y,data=data)
        g_2.set_xticklabels(g_2.get_xticklabels(),rotation=60)
        st.pyplot()
    else:
        st.header("Select at least one categorical and one numeric data series")




def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    """The file uploader widget does not provide information on the type of file uploaded so we have
    to guess using rules or ML. See
    [Issue 896](https://github.com/streamlit/streamlit/issues/896)

    I've implemented rules for now :-)

    Arguments:
        file {Union[BytesIO, StringIO]} -- The file uploaded

    Returns:
        FileType -- A best guess of the file type
    """
    content = file.getvalue()

    if ('xlsx' in file.name):
        return FileType.EXCEL

    return FileType.CSV


def translate_data(dataFrame):
    df = dataFrame.copy()
   
    return df

    


@st.cache(suppress_st_warning=True)    
def main():
    """Run this function to display the Streamlit app"""
    #st.info(__doc__)
    st.markdown(STYLE, unsafe_allow_html=True)

    file = st.file_uploader("Upload file", type=FILE_TYPES)
    show_file = st.empty()
    if not file:
        show_file.info("Please install the files that have these extensions: " + ", ".join(FILE_TYPES))
        return

    file_type = get_file_type(file)
    if file_type == FileType.IMAGE:
        show_file.image(file)
    elif file_type == FileType.PYTHON:
        st.code(file.getvalue())
    else:
        if file_type ==  FileType.CSV:
            try:
                data = pd.read_csv(file)
            except:
                data = pd.read_csv(file,error_bad_lines = False)


            data = translate_data(data)
            return data

            

        else: 
            try:
                data = pd.read_excel(file)
            except:
                try:
                    data = pd.read_excel(file,index_col=None, header=None)
                except:
                    data = pd.read_html(file)

          
            data = translate_data(data)
            return data
           



data = main()

x = st.selectbox("Select your x coordinate column name",data.columns)
y = st.selectbox("Select your y coordinate column name",data.columns)
z = st.selectbox("Select your hue related column name",data.columns)
plotData(data,x,y,z)

