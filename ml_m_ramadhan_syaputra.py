# -*- coding: utf-8 -*-
"""ML_M Ramadhan Syaputra.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PVMCXmqHY0lQAR4_tOunmc_5dBR8Rk1g

# Used Car Dataset
Dataset yang saya gunakan untuk Research ini adalah used_car_dataset.csv atau dataset yang berisikan data mobil bekas di pasar india. Dataset ini memiliki total data sebanyak 9,582 dengan 11 kolom, jika kita lihat berdasarkan isi data setiap kolom, dataset ini memiliki jenis data campuran. Disini saya akan melakukan Pre-processing data pada dataset ini dengan memanfaatkan beberapa library yang tersedia di dalam python, Tujuan yang akan saya lakukan untuk dataset ini adalah memprediksi harga mobil
"""

import pandas as pd
import numpy as np
import seaborn as sn
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

"""# Data Wrangling
Proses Data Wrangling ini meliputi
"""

df = pd.read_csv('/used_car_dataset.csv')
print (df.head(10))
print (df.info())

"""# 1
yang perlu kita lakukan adalah menghapus kolom yang tidak diperlukan untuk proses analisis

Jika tujuannya untuk memprediksi Harga , Kolom yang tidak diperlukan mencakup : AdditionInfo, Age dan PostedDate
"""

df.drop(['Age','PostedDate','AdditionInfo'],axis = 1,inplace= True)
df.head((10))

"""# 2
Selanjutnya adalah menghilangkan Missing Values, Jika kita lihat hanya kolom kmDriven yang memiliki missing values sebanyak 47, maka kita lakukan proses menambah missing values dengan menggunakan mean dari data kolom kmDriven
"""

print("\nMissing Values per Column Before Cleaning:")
print(df.isnull().sum())

# Mengubah Tipe Data Object menjadi String terlebih dahulu
df['kmDriven'] = df['kmDriven'].astype(str)
df['kmDriven'] = df['kmDriven'].str.replace('km', '').str.replace(',', '').astype(float)

df['AskPrice'] = df['AskPrice'].astype(str)
df['AskPrice'] = df['AskPrice'].str.replace('₹', '').str.replace(',', '').astype(float)

# Mengisi nilai yang hilang dengan rata-rata
df['kmDriven'] = df['kmDriven'].fillna(df['kmDriven'].mean())

print("\nMissing Values per Column After Cleaning:")
print (df.head(10))
print(df.isnull().sum())

"""# 3
Setelah Mengisi Missing Values, selanjutnya adalah menghapus data duplikat dan hasilnya dataset ini tidak memiliki data duplikat karena memiliki hasil yang sama
"""

print ("\nDataset sebelum menghapus duplikasi:")
print(df.shape)

# Menghapus data duplikat
df = df.drop_duplicates()

print("\nDataset setelah menghapus duplikasi:")
print(df.shape)

"""# 4
Merubah Isi data kolom Kategorikal menjadi numerik agar proses machine learning dapat terjalani, Kolom Owner, FuelType dan Transmission merupakan kolom kategorikal
"""

# Inisialisasi encoder
le = LabelEncoder()

# Mengubah kolom menjadi numerik
df['transmission_encoded'] = le.fit_transform(df['Transmission'])
df['fueltype_encoded'] = le.fit_transform(df['FuelType'])
df['owner_encoded'] = le.fit_transform(df['Owner'])

# Lihat hasil
print(df[['Transmission', 'transmission_encoded']].head())
print(df[['FuelType', 'fueltype_encoded']].head())
print(df[['Owner', 'owner_encoded']].head())

"""# 5
Normalisasi Data Numerik berguna agar model machine learning nantinya dapat mempercepat konvergensi dan meningkatkan kinerja model nantinya

Kolom yang perlu dinormalisasi pada dataset ini adalah kmDriven dan AskPrice
"""

# Normalisasi Min-Max
scaler = MinMaxScaler()
df[['kmDriven', 'AskPrice']] = scaler.fit_transform(df[['kmDriven', 'AskPrice']])

print(df)

"""# Data Availability Checking dan Descriptive Statistic
Setelah Proses Data Wrangling selesai selanjutnya kita melakukan pengecekan terhadap data apakah terdapat data yang null dan eror. Jika dilihat dari hasilnya eror dan null sudah diperbaiki
"""

# Informasi tentang kolom dan tipe data
print("\nDataset Info:")
print(df.info())

# Statistik deskriptif
print("\nDescriptive Statistics:")
print(df.describe())

# Mengecek jumlah nilai yang hilang
print("\nMissing Values per Column:")
print(df.isnull().sum())

"""# EDA dan Visualization Data
Selanjutnya adalah melihat korelasi pada data ini dan digambarkan dalam bentuk Visualisasi
"""

# Melihat struktur data
print(df.info())

# Melihat beberapa baris data
print(df.head())

# Melihat statistik deskriptif
print(df.describe(include='all'))

"""Menghitung Distribusi Untuk Data Kategorikal dan Numberik"""

# Distribusi data kategorikal
print(df['Transmission'].value_counts())
print(df['Owner'].value_counts())
print(df['FuelType'].value_counts())

# Histogram kmDriven
sns.histplot(df['kmDriven'], bins=10, kde=True)
plt.title('Distribusi kmDriven')
plt.show()

# Histogram AskPrice
sns.histplot(df['AskPrice'], bins=10, kde=True)
plt.title('Distribusi AskPrice')
plt.show()

"""Analisis Korelasi untuk data Numerik dan Kategorikal karena kolom kolom ini berpengaruh untuk menentukan Harga Mobil

Berdasarkan Visualisasi Datanya,Jenis transmisi dan jarak tempuh adalah faktor yang paling relevan terhadap harga kendaraan dalam dataset ini. Namun, pengaruhnya masih tergolong sedang hingga lemah, sehingga faktor tambahan mungkin diperlukan untuk memprediksi harga secara akurat.
"""

numerical = df[['kmDriven', 'AskPrice','transmission_encoded','owner_encoded','fueltype_encoded']]

# Matriks korelasi
correlation = numerical.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Matriks Korelasi')
plt.show()

"""Disini juga merupakan Visualisasi data AskPrice jika berdasrkan jenis bahan bakar

Untuk jenis transmisi juga dapat dilihat bahwa harga lebih tinggi jika jenis transmisinya automatic
"""

# Boxplot AskPrice berdasarkan FuelType
sns.boxplot(x='FuelType', y='AskPrice', data=df)
plt.title('Harga Mobil Berdasarkan Jenis Bahan Bakar')
plt.show()

# Barplot rata-rata harga berdasarkan Transmission
sns.barplot(x='Transmission', y='AskPrice', data=df)
plt.title('Rata-rata Harga Berdasarkan Transmisi')
plt.show()

"""Mendeteksi Outlier dan ternyata kedua data numerik ini memiliki outlier"""

# Boxplot untuk kmDriven
sns.boxplot(df['kmDriven'])
plt.title('Outlier pada kmDriven')
plt.show()

# Boxplot untuk AskPrice
sns.boxplot(df['AskPrice'])
plt.title('Outlier pada AskPrice')
plt.show()

"""Deteksi Anomali dan hasilnya semua data valid dan relevan"""

# Cek apakah ada mobil dengan tahun produksi lebih besar dari tahun sekarang
print(df[df['Year'] > 2024])

# Cek apakah ada harga atau kilometer yang sangat kecil atau besar
print(df[df['AskPrice'] < 10000])
print(df[df['kmDriven'] > 500000])
