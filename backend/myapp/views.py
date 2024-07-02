from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Veri setini yükleme
df = pd.read_csv("../data/musev3_spotify_dataset_20kSon.csv", encoding="utf-8")

# Verileri X ve y olarak ayırma
X = df[
    [
        "acousticness",
        "danceability",
        "energy",
        "liveness",
        "loudness",
        "tempo",
        "valence",
    ]
]
y = df["genre"]

# Sınıf etiketlerini sayısal değerlere dönüştürme
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Verileri standartlaştırma
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X = pd.DataFrame(X_scaled, columns=X.columns)

# Verileri eğitim ve test setleri olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Modeli yükleme veya oluşturma
model_path = "../model"
if os.path.exists(model_path):
    print("Kaydedilmiş model yükleniyor...")
    model = tf.keras.models.load_model(model_path)
else:
    # Fonksiyonel API kullanarak MLP modeli oluşturma
    inputs = tf.keras.Input(shape=(7,))
    x = tf.keras.layers.Dense(256, activation="relu")(inputs)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    x = tf.keras.layers.Dense(32, activation="relu")(x)
    outputs = tf.keras.layers.Dense(17, activation="softmax")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    # Modeli derleme
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    # Modeli eğitme
    model.fit(X_train, y_train, epochs=1500, validation_data=(X_test, y_test))
    # Modeli kaydetme
    model.save(model_path)


def get_audio_features(track_id):
    client_id = "51b917197a7a43c8ba1add0b311fa753"
    client_secret = "3fde411a25f3401090e096628542b19b"
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    features = sp.audio_features(track_id)[0]
    return [
        float(features["acousticness"]),
        float(features["danceability"]),
        float(features["energy"]),
        float(features["liveness"]),
        float(features["loudness"]),
        float(features["tempo"]),
        float(features["valence"]),
    ]


def get_track_photo(track_id):
    client_id = "51b917197a7a43c8ba1add0b311fa753"
    client_secret = "3fde411a25f3401090e096628542b19b"
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track = sp.track(track_id)
    photos = track["album"]["images"]
    if photos:
        return photos[0]["url"]
    return None


def music_similarity(muzik):
    muzik_df = pd.DataFrame([muzik], columns=X.columns)
    muzik_scaled = scaler.transform(muzik_df)
    tahmin = model.predict(muzik_scaled)
    tahmin = label_encoder.classes_[np.argmax(tahmin)]
    similarities = cosine_similarity(muzik_scaled, X_scaled)
    sorted_similarity_indices_and_values = sorted(
        enumerate(similarities[0]), key=lambda x: x[1], reverse=True
    )
    recommended_songs = []
    for index, similarity in sorted_similarity_indices_and_values[1:6]:
        song_info = df[["track", "artist", "spotify_id", "seeds", "genre"]].iloc[index]
        similarity_percentage = similarity * 100
        recommended_songs.append(
            {
                "Benzerlik Oranı": f"{similarity_percentage:.2f}%",
                "Track": song_info["track"],
                "Artist": song_info["artist"],
                "Spotify ID": song_info["spotify_id"],
                "Seeds": song_info["seeds"],
                "Genre": song_info["genre"],
                "cover": get_track_photo(song_info["spotify_id"]),
            }
        )
    return tahmin, recommended_songs


@api_view(["POST"])
def music_recommendation(request):
    try:
        spotify_link = request.data["spotify_link"]
        pattern = r"track/(\w+)"
        track_id = re.search(pattern, spotify_link)
        if track_id:
            track_id = track_id.group(1)
        else:
            return Response({"status": False, "message": "Spotify ID bulunamadı."})
        tahmin, recommended_songs = music_similarity(get_audio_features(track_id))
        return Response(
            {"status": True, "genre": tahmin, "recommended_songs": recommended_songs}
        )
    except Exception as ex:
        return Response({"status": False, "message": str(ex)})
