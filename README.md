
# Chat with MySQL (Backend) 

> Final Project Glue-4

Platform Chat with MySQL menggunakan python dan OpenAI API untuk membantu baca dan analisis database MySQL tanpa perlu menjadi ahli MySQL.

## ⚙️ Deployment

Untuk deploy, lakukan clone repo terlebih dahulu

```bash
  git clone https://github.com/Glue-4/back-end.git
```

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
