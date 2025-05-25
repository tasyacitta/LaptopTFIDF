import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if 'show_display' not in st.session_state:
    st.session_state.show_display = False
if 'show_price' not in st.session_state:
    st.session_state.show_price = False

def calculate_similarity( inputText,display, pricing):
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(data_spec['specification'])
        input_spec = f"{inputText} {display} {pricing}"
        Y = vectorizer.transform([input_spec])

        similarity_result = cosine_similarity(X, Y)
        similarity_result  = similarity_result .flatten()  # Ratakan array
        return similarity_result

with st.expander('Data Raw'):
    st.header("Data Raw")
    data_raw = pd.read_csv('complete laptop data0.csv', encoding = 'unicode_escape')
    data_raw
    st.write(f"Jumlah Baris dalam DataFrame: {data_raw.shape[0]}")
    st.write(f"Total Kolom dalam DataFrame: {data_raw.shape[1]}")

with st.expander('Data Clean'):
    st.header('Data Clean')
    data_clean = pd.read_csv('clean_data.csv', encoding='unicode_escape')
    data_clean
    st.write(f"Jumlah Baris dalam DataFrame: {data_clean.shape[0]}")
    st.write(f"Total Kolom dalam DataFrame: {data_clean.shape[1]}")

with st.expander('Data Specification'):
    st.header('Data Specification')
    data_spec = pd.read_csv('dataset_spec.csv', encoding='unicode_escape')
    data_spec
    st.write(f"Jumlah Baris dalam DataFrame: {data_spec.shape[0]}")
    st.write(f"Total Kolom dalam DataFrame: {data_spec.shape[1]}")

with st.form("form_input"):
    unique_display = sorted(filter(lambda x: x != ' ', data_clean['display'].unique()))
    unique_pricing = sorted(data_clean['pricing'].unique().tolist())
   

    inputText = st.text_input("Masukkan kriteria laptop")
    display_clicked = st.form_submit_button("Display")
    if display_clicked:
        st.session_state.show_display = not st.session_state.show_display

    # Price Button
    price_clicked = st.form_submit_button("Price")
    if price_clicked:
        st.session_state.show_price = not st.session_state.show_price
    # Dynamic fields based on button clicks
    selected_display = None
    selected_pricing = None

    if st.session_state.show_display:
        selected_display = st.selectbox("Pilih Display:", unique_display)

    if st.session_state.show_price:
        selected_pricing = st.selectbox("Pilih Rentang Harga:", unique_pricing)

    #selected_display = st.selectbox("Pilih Display:", unique_display)
    #selected_pricing = st.selectbox("Pilih Rentang Harga:", unique_pricing)

   
    submitted = st.form_submit_button("Submit")
    # Initialize session state if not already set

    if submitted:
# if st.button('Hitung Similarity'):
        similarity_new = calculate_similarity( inputText,selected_display, selected_pricing)
            
        # Menentukan reshape ukuran yang bagus
        rows = 10  # Jumlah baris
        cols = 10  # Jumlah kolom
        total_elements = rows * cols  # Total elemen dalam array reshaped

        # Jika similarity_new memiliki lebih dari 100 elemen, ambil 100 pertama, jika kurang, tambahkan dengan nol
        if similarity_new.size >= total_elements:
            similarity_reshaped = similarity_new[:total_elements].reshape(rows, cols)
        else:
            similarity_reshaped = np.pad(similarity_new, (0, total_elements - similarity_new.size), 'constant').reshape(rows, cols)

        # Sortir similarity_new untuk mendapatkan urutan kemiripan
        similarity_score = list(enumerate(similarity_new))  # Buat daftar tuple (index, score)
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)  # Urutkan dari yang tertinggi

        # Ambil indeks yang relevan dari hasil similarity_new
        indices_list = [index for index, score in similarity_score]  # Daftar indeks sesuai kemiripan

        # Ambil baris dari dataset_spec berdasarkan indeks tersebut, dan buat salinan
        df_similar_laptops = data_clean.iloc[indices_list].copy()  # Membuat salinan eksplisit

        # Tambahkan kolom skor kemiripan ke DataFrame
        df_similar_laptops['similarity_score'] = [score for index, score in similarity_score]

        # Tampilkan DataFrame dengan spesifikasi dan skor kemiripan
        with st.expander("Urutan Hasil Rekomendasi Laptop"):
            st.header("Urutan Hasil Rekomendasi Laptop")
            df_similar_laptops
            st.write(f"Jumlah Baris dalam DataFrame: {data_clean.shape[0]}")

        with st.expander("Hasil Cosine Similarity"):
            st.header("Hasil Cosine Similarity")
            similarity_reshaped
            st.write(f"Jumlah Baris dalam DataFrame: {data_clean.shape[0]}")
