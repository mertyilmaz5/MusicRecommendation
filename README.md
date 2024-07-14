# Music Recommendation

Bu proje, Django backend, React frontend ve TensorFlow modeli içeren bir makine öğrenimi projesidir. Proje, kullanıcıların Spotify şarkılarını analiz edip benzer şarkıları önermektedir.

## Proje Yapısı

- **backend/**: Django backend uygulaması ve gerekli dosyalar.
- **data/**: Modelin çalıştığı veri seti.
- **frontend/**: React frontend uygulaması ve gerekli dosyalar.
- **model/**: Eğitilmiş model dosyaları.
- **env/**: Python sanal ortamı.

## Kurulum

### Gerekli Yazılımlar

- Python 3.10
- Node.js ve npm
- Git

### Adımlar

1. Projeyi klonlayın:

   ```bash
   git clone https://github.com/mertyilmaz5/MusicRecommendation.git
   cd MusicRecommendation
   ```

2. Python sanal ortamı oluşturun ve gerekli paketleri yükleyin:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Windows için: myenv\Scripts\activate
   cd backend
   pip install -r requirements.txt
   ```

3. Frontend bağımlılıklarını yükleyin:

   ```bash
   cd frontend
   npm install
   ```

4. Django veritabanını oluşturun ve migrasyonları çalıştırın:

   ```bash
   cd ../backend
   python manage.py makemigrations
   python manage.py migrate
   ```

## Kullanım

1. Backend sunucusunu başlatın:

   ```bash
   cd backend
   python manage.py runserver
   ```

2. Frontend uygulamasını başlatın:

   ```bash
   cd ../frontend
   npm start
   ```

3. Web tarayıcınızda `http://localhost:3000` adresine gidin.

## Katkıda Bulunma

Katkıda bulunmak isterseniz lütfen bir `issue` açın veya `pull request` gönderin.

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
