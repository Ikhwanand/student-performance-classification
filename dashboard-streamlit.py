import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# Load model dan pipeline
@st.cache_resource
def load_models():
    model = joblib.load('./models/final_lr_model.pkl')
    pipeline = joblib.load('./models/preprocessing_pipeline.pkl')
    label_encoder = joblib.load('./models/label_encoder.pkl')
    return model, pipeline, label_encoder

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('./data/data.csv', sep=';')
    return df

# Main function
def main():
    st.title("Dashboard Prediksi Perform Siswa")
    st.sidebar.title("Menu")
    
    # Load data dan mode
    df = load_data()
    model, pipeline, label_encoder = load_models()
    
    # Menu sidebar
    menu = st.sidebar.radio(
        'Pilih Halaman:',
        ['Beranda', 'Eksplorasi Data', 'Prediksi Status Siswa']
    )
    
    if menu == 'Beranda':
        show_home_page(df)
    elif menu == 'Eksplorasi Data':
        show_exploration_page(df)
    else:
        show_prediction_page(df, model, pipeline, label_encoder)
        

def show_home_page(df):
    st.header("Sistem Prediksi Performa Akademik Siswa")
    st.write(
        """
        Dashboard ini membantu mengidentifikasi faktor-faktor yang mempengaruhi performa akademik siswa
        dan memprediksi status siswa (Dropout, Enrolled, atau Graduate) berdasarkan berbagai fitur.
        """
    )
    
    # Tampilkan ringkasan dataset
    st.subheader("Ringkasan Dataset")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jumlah Siswa", df.shape[0])
    with col2:
        st.metric("Dropout Rate", f"{df[df['Status'] == 'Dropout'].shape[0]/df.shape[0]:.1%}")
    with col3:
        st.metric("Graduate Rate", f"{df[df['Status'] == 'Graduate'].shape[0]/df.shape[0]:.1%}")
    
    # Visualisasi distribusi status
    st.subheader("Distribusi Status Siswa")
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig = px.pie(status_counts, values='Count', names='Status',
                 title='Distribusi Status Siswa',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig)
    

def show_exploration_page(df):
    st.header("Eksplorasi Data")
    
    # Pilihan visualisasi
    viz_option = st.selectbox(
        'Pilih Visualisasi:',
        ['Performa Akademik', 'Faktor Sosio-Ekonomi', 'Korelasi Fitur']
    )
    
    if viz_option == 'Performa Akademik':
        st.subheader('Performa Akademik Berdasarkan Status')
        
        # Pilih semester
        semester = st.radio('Pilih Semester:', ['Semester 1', 'Semester 2'])
        
        if semester == 'Semester 1':
            col_grade = 'Curricular_units_1st_sem_grade'
            col_approved = 'Curricular_units_1st_sem_approved'
        else:
            col_grade = 'Curricular_units_2nd_sem_grade'
            col_approved = 'Curricular_units_2nd_sem_approved'
        
        # Visualisasi nilai
        fig1 = px.box(df, x='Status', y=col_grade,
                      title=f'Distribusi Nilai {semester} Berdasarkan Status',
                      color='Status')
        st.plotly_chart(fig1)
        
        # Visualisasi unit yang disetujui
        fig2 = px.box(df, x='Status', y=col_approved,
                      title=f'Distribusi Unit yang Disetujui {semester} Berdasarkan Status',
                      color='Status')
        st.plotly_chart(fig2)
    
    elif viz_option == 'Faktor Sosio-Ekonomi':
        st.subheader('Faktor Sosio-Ekonomi Berdasarkan Status')
        
        # Pilih faktor
        factor = st.selectbox(
            'Pilih Faktor:',
            ['Scholarship_holder', 'Debtor', 'Tuition_fees_up_to_date', 'Age_at_enrollment']
        )
        
        if factor in ['Scholarship_holder', 'Debtor', 'Tuition_fees_up_to_date']:
            # Visualisasi untuk faktor kategorikal
            factor_counts = df.groupby(['Status', factor]).size().reset_index(name='count')
            fig = px.bar(factor_counts, x='Status', y='count', color=factor,
                         barmode='group', title=f'Distribusi {factor} Berdasarkan Status')
            st.plotly_chart(fig)
        else:
            # Visualisasi untuk faktor numerik (Age)
            fig = px.histogram(df, x=factor, color='Status',
                               marginal='box', title=f'Distribusi {factor} Berdasarkan Status')
            st.plotly_chart(fig)
    
    else: # Korelasi Fitur
        st.subheader('Korelasi Fitur dengan Status Siswa')
        
        # Membuat DataFrame dengan variabel target numerik
        df_numeric = df.copy()
        df_numeric['Status_numeric'] = df_numeric['Status'].map({'Dropout': 0, 'Graduate': 1, 'Enrolled': 0.5})
        
        # Memilih hanya kolom numerik untuk korelasi
        numeric_cols = df_numeric.select_dtypes(include=['float64', 'int64']).columns
        
        # Menghitung korelasi dengan target
        correlation_with_target = df_numeric[numeric_cols].corr()['Status_numeric'].sort_values(ascending=False)
        correlation_with_target = correlation_with_target.drop('Status_numeric') # Menghapus self-correlation
        
        # Filter korelasi yang > 0.1 atau < -0.1
        correlation_with_target = correlation_with_target[abs(correlation_with_target) > 0.1]
        
        # Visualisasi korelasi
        fig = px.bar(
            x=correlation_with_target.values,
            y=correlation_with_target.index,
            orientation='h',
            title='Korelasi Fitur dengan Status Siswa',
            labels={'x': 'Korelasi', 'y': 'Fitur'}
        )
        fig.add_vline(x=0, line_width=1, line_dash='dash', line_color='red')
        st.plotly_chart(fig)
    

def show_prediction_page(df, model, pipeline, label_encoder):
    st.header('Prediksi Status Siswa')
    st.write('Masukkan informasi siswa untuk memprediksi statusnya')
    
    # buat form input
    with st.form('prediction_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input('Usia saat pendaftaran', min_value=17, max_value=70, value=20)
            marital_status = st.selectbox('Status Pernikahan', options=[1, 2, 3, 4, 5, 6], index=0)
            application_mode = st.selectbox('Mode Aplikasi', options=sorted(df['Application_mode'].unique()), index=0)
            course = st.selectbox('Kursus', options=sorted(df['Course'].unique()), index=0)
            previous_qualification = st.selectbox('Kualifikasi Sebelumnya', options=sorted(df['Previous_qualification'].unique()), index=0)
            scholarship = st.selectbox('Penerima Beasiswa', options=[0, 1], index=0)
        
        with col2:
            debtor = st.selectbox('Status Hutang', options=[0, 1], index=0)
            tuition_up_to_date = st.selectbox('SPP Terbayar', options=[0, 1], index=1)
            gender = st.selectbox('Jenis Kelamin', options=[0, 1], index=0)
            sem1_grade = st.number_input('Nilai Semester 1', min_value=0.0, max_value=20.0, value=12.0, step=0.1)
            sem1_approved = st.number_input('Unit Disetujui Semester 1', min_value=0, max_value=20, value=5)
            sem2_approved = st.number_input('Unit Disetujui Semester 2', min_value=0, max_value=20, value=5)
        
        submit_button = st.form_submit_button(label='Prediksi')
    
    if submit_button:
        # buat data input
        input_data = {
            'Age_at_enrollment': age,
            'Marital_status': marital_status,
            'Application_mode': application_mode,
            'Course': course,
            'Previous_qualification': previous_qualification,
            'Scholarship_holder': scholarship,
            'Debtor': debtor,
            'Tuition_fees_up_to_date': tuition_up_to_date,
            'Gender': gender,
            'Curricular_units_1st_sem_grade': sem1_grade,
            'Curricular_units_1st_sem_approved': sem1_approved,
            'Curricular_units_2nd_sem_approved': sem2_approved
        }
        
        # Tambahkan kolom lain dengan nilai default
        for col in df.columns:
            if col not in input_data and col != 'Status':
                input_data[col] = df[col].median() if df[col].dtype in ['int64', 'float64'] else df[col].mode()[0]
                
        # Buat DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Preprocessing dan prediksi
        try:
            input_processed = pipeline.transform(input_df)
            prediction_encoded = model.predict(input_processed)[0]
            prediction_proba = model.predict_proba(input_processed)[0]
            prediction = label_encoder.inverse_transform([prediction_encoded])[0]
            
            # Tampilkan hasil
            st.success(f'Prediksi Status: **{prediction}**')
            
            # Visualisasi probabilitas
            proba_df = pd.DataFrame({
                'Status': label_encoder.classes_,
                'Probability': prediction_proba
            })
            
            fig = px.bar(proba_df, x='Status', y='Probability',
                         title='Probabilitas Prediksi',
                         color='Status')
            st.plotly_chart(fig)
            
            # Interpretasi
            st.subheader('Interpretasi Hasil')
            if prediction == 'Dropout':
                st.warning('Siswa ini berisiko dropout. Pertimbangkan untuk memberikan dukungan tambahan.')
            elif prediction == 'Enrolled':
                st.info('Siswa ini kemungkinan akan tetap terdaftar. Pantau perkembangannya.')
            else:
                st.success('Siswa ini memiliki prospek baik untuk lulus. Terus dukung prestasinya.')
            
        except Exception as e:
            st.error(f'Terjadi kesalahan dalam prediksi: {e}')
            

if __name__ == '__main__':
    main()