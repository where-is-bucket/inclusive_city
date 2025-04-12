import React from "react";
import { FiMapPin, FiClock, FiPhone, FiGlobe, FiStar } from "react-icons/fi";

const OverviewTab = ({ selectedMarker }) => {
    const powerIndexPercent = selectedMarker.accessibility_rate * 100; // Значення від 0 до 100
    const powerData = [
        "Вхід безперешкодний, врівень з землею",
        "Вхідні двері шириною не менше 0,9 м",
        "Коридори шириною не менше 1,8 м",
        "Засоби візуальної орієнтації (інформаційні покажчики, стенди)",
        "Ширина тротуару перед будівлею не менше 1.8 м",
        "Тротуар рівний, без вибоїн, має тверде безфаскове покриття",
    ];

    // Функція для визначення кольору маркера
    const getMarkerColor = (percent) => {
        if (percent < 20) return '#ff0000';
        if (percent < 40) return '#ff8000';
        if (percent < 60) return '#ffff00';
        if (percent < 80) return '#80ff00';
        return '#00ff00';
    };

    return (
        <div className="overview">
            <div className="overview__section">
                <div className="overview__info-item">
                    <div className="overview__info-icon">
                        <FiMapPin/>
                    </div>
                    <div className="overview__info-text">
                        {selectedMarker.address}
                    </div>
                </div>

                {selectedMarker.phone && (
                    <div className="overview__info-item">
                        <div className="overview__info-icon">
                            <FiPhone/>
                        </div>
                        <div className="overview__info-text">
                            <a href={`tel:${selectedMarker.phone}`}>{selectedMarker.phone}</a>
                        </div>
                    </div>
                )}

                {selectedMarker.website && (
                    <div className="overview__info-item">
                        <div className="overview__info-icon">
                            <FiGlobe/>
                        </div>
                        <div className="overview__info-text">
                            <a href={selectedMarker.website} target="_blank" rel="noopener noreferrer"
                               className="overview__link">
                                {selectedMarker.website.replace(/^https?:\/\//, '')}
                            </a>
                        </div>
                    </div>
                )}

                {selectedMarker.rating && (
                    <div className="overview__info-item">
                        <div className="overview__info-icon">
                            <FiStar/>
                        </div>
                        <div className="overview__info-text">
                            Рейтинг: {selectedMarker.rating} ★
                        </div>
                    </div>
                )}
            </div>

            {selectedMarker.description && (
                <div className="overview__section">
                    <h3 className="overview__section-title">Опис</h3>
                    <p>{selectedMarker.description}</p>
                </div>
            )}

            <div className="overview__section">
                <div className="power-index-header">
                    <div className="overview__section-title">Індекс безбар'єрності</div>
                    <span className="power-index-percent">{powerIndexPercent}%</span>
                </div>
                <div className="power-index">
                    <div className="power-index__scale">
                        <div className="power-index__marker"
                             style={{
                                 left: `${powerIndexPercent}%`,
                                 backgroundColor: getMarkerColor(powerIndexPercent)
                             }}>
                        </div>
                    </div>
                    <ul className="power-data">
                        {selectedMarker?.facilities?.map((facility) => (
                            <li key={facility.facility_id} className="power-data__item">
                                {facility.descriptive_name}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default OverviewTab;