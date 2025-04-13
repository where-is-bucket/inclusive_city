import React, {useState} from "react";
import ReviewsTab from "./components/CommentsTab";
import OverviewTab from "./components/OverviewTab";
import {IoClose, IoArrowBack} from "react-icons/io5";
import {FaRoute, FaLocationArrow, FaSpinner} from "react-icons/fa";
import DefaultImg from "../../assets/img/default_geocode.png";

const TAB_OVERVIEW = 'overview';
const TAB_REVIEWS = 'reviews';

const SideMenu = ({
                      selectedMarker,
                      isOpen,
                      onClose,
                      routeMode,
                      setRouteMode,
                      fromAddress,
                      setFromPoint,
                      setFromAddress,
                      toAddress,
                      setToPoint,
                      setToAddress,
                      onSubmitRoute,
                      isLoadingRoute,
                      refetchPlace,
                      availableFacilities,
                      setFacilitiesForMarker,
                  }) => {
    const [activeTab, setActiveTab] = useState(TAB_OVERVIEW);

    const handleRouteClick = () => {
        setRouteMode(true);
        setToAddress(selectedMarker.address);
        setToPoint({
            lat: selectedMarker.location.latitude,
            lng: selectedMarker.location.longitude
        })
    };

    const handleBackClick = () => {
        setRouteMode(false);
    };

    const handleCurrentLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setFromPoint({ lat: latitude, lng: longitude });
                    setFromAddress("Моє місцезнаходження");
                },
                (error) => {console.log(error)},
                {timeout: 5000}
            );
        } else {
            alert("Геолокація не підтримується вашим браузером");
        }
    };

    return (
        <div className={`side-menu ${isOpen ? 'side-menu--open' : ''}`}>
            <button className="side-menu__close-btn" onClick={onClose}>
                <IoClose size={24}/>
            </button>

            {selectedMarker ? (
                <div className="side-menu__content-wrap">
                    {!routeMode ? (
                        <>
                            <div className="side-menu__photo-container">
                                <img
                                    src={selectedMarker.google_photo_url ?? DefaultImg}
                                    alt={selectedMarker.place_name}
                                    className="side-menu__photo"
                                />
                            </div>

                            <div className="side-menu__content">
                                <h2 className="side-menu__title">
                                    {selectedMarker.place_name}
                                </h2>

                                <button
                                    className="side-menu__route-btn"
                                    onClick={handleRouteClick}
                                >
                                    <FaRoute className="route-icon"/>
                                    <span>Прокласти маршрут</span>
                                </button>

                                <div className="side-menu__tabs">
                                    <button
                                        className={`side-menu__tab ${activeTab === TAB_OVERVIEW && 'side-menu__tab--active'}`}
                                        onClick={() => setActiveTab(TAB_OVERVIEW)}
                                    >
                                        Огляд
                                    </button>
                                    <button
                                        className={`side-menu__tab ${activeTab === TAB_REVIEWS && 'side-menu__tab--active'}`}
                                        onClick={() => setActiveTab(TAB_REVIEWS)}
                                    >
                                        Відгуки
                                    </button>
                                </div>

                                <div className="side-menu__tab-content">
                                    {activeTab === TAB_OVERVIEW ? (
                                        <OverviewTab
                                            selectedMarker={selectedMarker}
                                            availableFacilities={availableFacilities}
                                            setFacilitiesForMarker={setFacilitiesForMarker}
                                        />
                                    ) : (
                                        <ReviewsTab selectedMarker={selectedMarker} refetchPlace={refetchPlace}/>
                                    )}
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="side-menu__route-content">
                            <button
                                className="side-menu__back-btn"
                                onClick={handleBackClick}
                            >
                                <IoArrowBack size={20}/>
                                <span>Назад</span>
                            </button>

                            <h2 className="side-menu__title">Прокласти маршрут</h2>

                            <form onSubmit={onSubmitRoute} className="route-form">
                                <div className="route-form__group">
                                    <div className="route-form__label-wrapper">
                                        <label htmlFor="from-address" className="route-form__label">
                                            <span className="route-marker blue-marker"></span>
                                            Від:
                                        </label>
                                        <button
                                            type="button"
                                            className="route-form__location-btn"
                                            onClick={handleCurrentLocation}
                                        >
                                            <FaLocationArrow size={14}/>
                                            <span>Моє місце</span>
                                        </button>
                                    </div>
                                    <input
                                        id="from-address"
                                        type="text"
                                        value={fromAddress}
                                        onChange={(e) => setFromAddress(e.target.value)}
                                        className="route-form__input"
                                        placeholder="Клікніть на карту або введіть адресу"
                                        required
                                    />
                                </div>

                                <div className="route-form__group">
                                    <label htmlFor="to-address" className="route-form__label">
                                        <span className="route-marker yellow-marker"></span>
                                        До:
                                    </label>
                                    <input
                                        id="to-address"
                                        type="text"
                                        value={toAddress}
                                        readOnly
                                        className="route-form__input"
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="route-form__submit-btn"
                                    disabled={isLoadingRoute}
                                >
                                    {isLoadingRoute ? (
                                        <div className="loading-icon">
                                            <FaSpinner className="spin"/>
                                        </div>
                                    ) : (
                                        'Побудувати маршрут'
                                    )}
                                </button>
                            </form>
                        </div>
                    )}
                </div>
            ) : (
                <p className="side-menu__no-place">Оберіть місце</p>
            )}
        </div>
    );
};

export default SideMenu;