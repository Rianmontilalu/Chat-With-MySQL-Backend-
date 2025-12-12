
# Chat with MySQL (Backend) 

> Final Project

Platform Chat with MySQL menggunakan python dan OpenAI API untuk membantu baca dan analisis database MySQL tanpa perlu menjadi ahli MySQL.
Arsitektur Sistem 
● Frontend: Streamlit 
● Backend: LangChain + OpenAI API 
● Database: MySQL 

Deployment: 
○ Lokal untuk pengembangan awal 
○ AWS EC2 sebagai server untuk web app 
○ AWS RDS untuk MySQL 
  
Teknologi dan Alat yang Digunakan 
● Python: Bahasa pemrograman utama. 
● Streamlit: Untuk antarmuka pengguna. 
● LangChain: Untuk mengelola integrasi dengan OpenAI API. 
● OpenAI API: Untuk model bahasa. 
● MySQL: Untuk penyimpanan data. 
● AWS EC2: Untuk hosting aplikasi. 
● AWS RDS MySQL: Untuk hosting database. 

## ⚙️ Deployment

Buat file .env pada folder dan hirarki yang sama untuk API key dari OpenAI API *(Jangan lupa taruh API key milikmu)*

```bash
  echo OPENAI_API_KEY=GANTI_DENGAN_API_MILIKMU >> .env
```

Build image docker dengan nama `be-chat-mysql`

```bash
  docker run -t be-chat-mysql .
```

Jalankan docker menggunakan docker compose agar **environment** dan **port forwarding** berjalan

```bash
  docker-compose up
```
## 🖥️ Contoh Penggunaan

Pada penggunaannya gunakan aplikasi **Postman** atau sejenisnya, hubungkan ke url `http://localhost:8000/query` atau url lainnya *(Jika diatur berbeda)*, gunakan template file json dibawah ini untuk menggunakan API!

```
{
  "question" : " ",
  "user" : " ",
  "password" : " ",
  "host" : " ",
  "database" : " ",
  "port" : " ",
}
```

Isi bagian kosong dengan pertanyaan dan data dari database MySQL milikmu!

## ❗ Hal Penting 

Perhatikan beberapa hal berikut!

- Pastikan nama variabel pada file  `.env ` adalah  `OPENAI_API_KEY`

- Masukkan data dari database yang valid!.

- Port forwarding diatur pada port `8000`, kamu bisa menggantinya pada file `main.py` sesukamu. *(re-build image)*
