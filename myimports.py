import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import mysql.connector as mysql
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Text, String, DateTime, Boolean
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
from fonts import large_font, medium_font, small_bold
from myconnections import server_details, sqlalc_eng
import dataframe_image as dfi
import io as io

# Import regression training libraries and packages
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


# Import classification training libraries and packages
from sklearn.preprocessing import StandardScaler, MinMaxScaler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
# Packages for displaying classification accuracy
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
np.set_printoptions(suppress=True)


# Import clustering packages
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering