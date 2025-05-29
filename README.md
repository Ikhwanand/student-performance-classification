# Proyek Akhir: Menyelesaikan Permasalahan Jaya Jaya Institut

## Business Understanding
Jaya Jaya Institut menghadapi tantangan dalam meningkatkan tingkat kelulusan dan menurunkan angka dropout mahasiswa. Dengan banyaknya data akademik, sosio-ekonomi, dan demografi yang tersedia, institusi ingin memahami faktor-faktor utama yang memengaruhi performa mahasiswa serta membangun sistem prediksi status mahasiswa untuk mendukung pengambilan keputusan dan intervensi dini.

### Permasalahan Bisnis
- Tingginya tingkat dropout mahasiswa yang berdampak pada reputasi dan efisiensi institusi.
- Kurangnya pemahaman mendalam tentang faktor-faktor utama yang menyebabkan mahasiswa gagal lulus tepat waktu atau keluar dari institusi.
- Belum adanya sistem prediksi yang dapat membantu mengidentifikasi mahasiswa berisiko tinggi secara proaktif.

### Cakupan Proyek
- Eksplorasi dan analisis data mahasiswa (EDA) untuk menemukan pola dan insight penting.
- Pra-pemrosesan data: penanganan missing value, encoding variabel kategorikal, normalisasi fitur numerik.
- Pengembangan dan evaluasi model machine learning (Random Forest, Logistic Regression, XGBoost) untuk prediksi status mahasiswa (Dropout, Enrolled, Graduate).
- Pembuatan dashboard interaktif berbasis Streamlit untuk visualisasi data dan prediksi status mahasiswa.

### Persiapan
Sumber data: [Link Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv) (37 kolom, 4424 baris, berisi data demografi, akademik, ekonomi, dan status mahasiswa). Dokumentasi fitur tersedia di `data/data-information.md`.

Setup environment:
- Python 3.11+
- Library utama: pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, streamlit, joblib

Untuk setup environment, Anda dapat menggunakan `venv` atau `conda`.

**Menggunakan venv:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Menggunakan conda:**
```bash
conda create -n student_perf python=3.11
conda activate student_perf
pip install -r requirements.txt
```

- Instalasi dependensi: `pip install -r requirements.txt`

## Business Dashboard & Sistem Machine Learning
Sistem Machine Learning interaktif dibuat menggunakan Streamlit (<mcfile name="dashboard-streamlit.py" path="d:/student-performance-classification/dashboard-streamlit.py"></mcfile>). Fitur utama sistem:
- **Beranda:** Ringkasan dataset, distribusi status mahasiswa (Dropout, Graduate, Enrolled).
- **Eksplorasi Data:** Visualisasi interaktif performa akademik, faktor sosio-ekonomi, dan korelasi fitur dengan status mahasiswa.
- **Prediksi Status Mahasiswa:** Form input untuk prediksi status mahasiswa baru menggunakan model Logistic Regression terlatih, lengkap dengan visualisasi probabilitas dan interpretasi hasil.
- Visualisasi menggunakan Plotly untuk pengalaman eksplorasi data yang dinamis.

Untuk menjalankan sistem:
```bash
streamlit run dashboard-streamlit.py
```

Sedangkan untuk visualisasi dashboard yang tampilkan:

1. **Gambaran Umum**
    - Distribusi Status Siswa
    - Distribusi Mata kuliah berdasarkan status akademik siswa
    - Distribusi jenis kelamin berdasarkan status akademik siswa
    - Distribusi status pernikahan orang tua berdasarkan status akademik siswa

2. **Faktor Akademik**
    - Distribusi kualifikasi yang diterima sebelum mendaftar universitas berdasarkan status akademik siswa
    - Distribusi nilai lulusan penerimaan universitas berdasarkan status akademik siswa

3. **Faktor Sosio-Ekonomi**
    - Distribusi jenis pekerjaan orang tua berdasarkan status akademik siswa
    - Distribusi siswa yang memiliki hutang biaya sekolah berdasarkan status akademik siswa
    - Distribusi siswa yang mendapatkan beasiswa berdasarkan status akademik siswa
    - Distribusi siswa yang membayar biaya sekolah tepat waktu berdasarkan status akademik siswa
    - Distribusi umur siswa ketika mendaftar universitas
    
Berikut link untuk mengakses dashboard looker studio: [Looker Studio Dashboard](https://lookerstudio.google.com/reporting/d753c945-559b-46af-ba65-9d13bf43fbab)

<<<<<<< HEAD
## Menjalankan Machine Learning Yang Telah Dilatih
=======
Berikut link untuk mengakses dashboard streamlit: [Dashboard Streamlit](https://student-performance-classification-czj3a5sx23cqmupbatxnph.streamlit.app/)

## Menjalankan Sistem Machine Learning
>>>>>>> be447128c0a5058138e7d02495bad28db8f63f50
Model machine learning (Logistic Regression) beserta pipeline preprocessing dan label encoder telah disimpan di folder `models/`.
- File model: `models/final_lr_model.pkl`
- Pipeline preprocessing: `models/preprocessing_pipeline.pkl`
- Label encoder: `models/label_encoder.pkl`

Proses prediksi dapat dilakukan langsung melalui dashboard Streamlit. Untuk pelatihan ulang atau eksperimen model, gunakan notebook <mcfile name="notebook-1.ipynb" path="d:/student-performance-classification/notebook-1.ipynb"></mcfile>.

## Conclusion
Proyek ini berhasil membangun sistem prediksi status mahasiswa berbasis machine learning yang terintegrasi dalam dashboard interaktif. Hasil analisis menunjukkan beberapa faktor utama yang berkontribusi pada status mahasiswa, seperti performa akademik semester awal, status pembayaran SPP, dan penerimaan beasiswa. Dashboard yang dibuat memudahkan pihak institusi untuk melakukan monitoring, eksplorasi data, dan prediksi secara real-time.

### Rekomendasi Action Items
- Lakukan monitoring rutin terhadap mahasiswa dengan risiko dropout tinggi berdasarkan hasil prediksi dashboard.
- Terapkan intervensi dini (konseling, bantuan finansial, mentoring) untuk mahasiswa yang teridentifikasi berisiko.
- Lakukan evaluasi berkala terhadap model dan dashboard seiring bertambahnya data baru.
- Kembangkan fitur dashboard lebih lanjut, misal integrasi dengan sistem akademik atau penambahan analisis faktor eksternal.


        
