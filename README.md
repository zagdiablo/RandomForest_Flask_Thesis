
# Random Forest Algorithm Flask (Thesis)

Implementasi machine learning prediksi harga perumahan wilayah tangerang selatan menggunakan algoritma random forest melalui framework website Flask Python

## Run Locally

Clone the project

```bash
https://github.com/zagdiablo/RandomForest_Flask_Thesis.git
```

Sebelum melakukan perubahan pada kode, pastikan anda menggunakan branch "development"

```bash
git checkout development
```

Go to the project directory

```bash
cd /into/directory/RandomForest_Flask_Thesis
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
python run.py
```

## Documentation

Untuk front-end lokasi file adalah sebagai berikut:

- HTML ada di folder "templates".
- JS, CSS, IMG ada di folder "static".

cara memanggil file img/css/js, contoh memanggil file css:

Dari:

`<link rel="stylesheet" href="css/style.css" />`

Menjadi:

`<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />`

tambahkan `{{ url_for('static', filename='<lokasi/nama_file>') }}` pada href.
