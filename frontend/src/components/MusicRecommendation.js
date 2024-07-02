import React, { useState } from "react";
import axios from "axios";
import { FaSearch } from "react-icons/fa";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { Card, Row, Col } from "react-bootstrap";
import "./MusicRecommendation.css";

const MusicRecommendation = () => {
    const [spotifyLink, setSpotifyLink] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState(null);

    const handleChange = (e) => {
        setSpotifyLink(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const res = await axios.post("http://localhost:8000/music", {
                spotify_link: spotifyLink,
            });
            setResponse(res.data);
            console.log(res.data);
        } catch (error) {
            setResponse({
                status: false,
                message: "Bir hata oluştu. Lütfen tekrar deneyin.",
            });
        }
        setIsLoading(false);
    };

    return (
        <div className="main-container">
            <div className="content">
                <h1 className="title">Müzik Öneri Uygulaması</h1>
                <form onSubmit={handleSubmit} className="search-form">
                    <div className="input-group">
                        <input
                            type="text"
                            className="form-control input-url"
                            placeholder="Spotify Linki Giriniz..."
                            value={spotifyLink}
                            onChange={handleChange}
                        />
                        <button
                            type="submit"
                            className="btn btn-primary search-button"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <AiOutlineLoading3Quarters className="loading-icon" />
                            ) : (
                                <FaSearch />
                            )}
                        </button>
                    </div>
                </form>

                {response && (
                    <>
                        <h4 className="suggested-songs-title">
                            Aradığınız şarkıya uygun öneriler:
                        </h4>
                        <div className="song-results">
                            {response.recommended_songs.map((song, index) => {
                                const seedsArray = Array.isArray(song.Seeds)
                                    ? song.Seeds
                                    : song.Seeds.split(",").map((seed) =>
                                        seed.replace(/[^\w\s]/g, "")
                                    );

                                return (
                                    <Card className="music-card my-3" key={index}>
                                        <Card.Body>
                                            <Row style={{ marginBlock: 1 }}>
                                                <Col xs={3}>
                                                    <img
                                                        className="img-fluid"
                                                        src={song.cover}
                                                        alt="cover"
                                                    />
                                                </Col>
                                                <Col xs={7} style={{ textAlign: "left" }}>
                                                    <Card.Title>{song.Track}</Card.Title>
                                                    <Card.Text>{song.Artist}</Card.Text>
                                                </Col>
                                                <Col
                                                    xs={2}
                                                    className="text-right"
                                                    style={{
                                                        justifyContent: "space-between",
                                                        margin: "auto",
                                                    }}
                                                >
                                                    <Card.Text>
                                                        <i>{song.Genre}</i>
                                                    </Card.Text>
                                                    <Card.Text
                                                        style={{
                                                            border: "1px solid #D1D1D1",
                                                            borderRadius: ".5rem",
                                                        }}
                                                    >
                                                        <b>{song["Benzerlik Oranı"]}</b>
                                                    </Card.Text>
                                                </Col>
                                            </Row>
                                        </Card.Body>
                                        <Card.Footer>
                                            <h6 className="text-dark">
                                                Duygu Etiketi: <b>{seedsArray.join(", ")}</b>
                                            </h6>
                                        </Card.Footer>
                                    </Card>
                                );
                            })}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default MusicRecommendation;
