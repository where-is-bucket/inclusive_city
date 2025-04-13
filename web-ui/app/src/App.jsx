import React, {useState, useEffect} from "react";
import {
    Map,
    AdvancedMarker, Pin,
} from '@vis.gl/react-google-maps';
import './App.css';
import {getPlaces, getPlaceById} from "./api/places-api.js";
import SideMenu from "./components/SideMenu/index.jsx";
import {FiChevronLeft, FiChevronRight} from "react-icons/fi";
import {decodePolyline} from "./services/polyline-service.js";
import {Polyline} from "./components/GoogleMap/Polyline/index.jsx";
import {getRoute} from "./api/direction-api.js";
import {GOOGLE_MAP_ID} from './config';

const DISABILITY_TYPE_VISUAL_IMPAIRMENT = 'Visual Impairment';
const DISABILITY_TYPE_HEARING_IMPAIRMENT = 'Hearing Impairment';
const DISABILITY_TYPE_MOBILITY_IMPAIRMENT = 'Mobility Impairment';

export default function App() {
    const [markers, setMarkers] = useState([]);
    const [filteredMarkers, setFilteredMarkers] = useState([]);
    const [selectedMarker, setSelectedMarker] = useState(null);
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isFilterOpen, setIsFilterOpen] = useState(false);
    const [routeMode, setRouteMode] = useState(false);
    const [fromPoint, setFromPoint] = useState(null);
    const [toPoint, setToPoint] = useState(null);
    const [fromAddress, setFromAddress] = useState('');
    const [toAddress, setToAddress] = useState('');
    const [filters, setFilters] = useState({
        visualImpairment: false,
        hearingImpairment: false,
        mobilityImpairment: false
    });
    const [route, setRoute] = useState(null);
    const [isLoadingRoute, setIsLoadingRoute] = useState(false);

    const fetchMarkers = async () => {
        const response = await getPlaces();
        setMarkers(response.data)
    }

    const fetchMarker = async (place_id) => {
        try {
            const response = await getPlaceById({ params: { place_id } });
            const updatedMarker = response.data;

            setMarkers(prevMarkers => {
                const markerIndex = prevMarkers.findIndex(m => m.place_id === place_id);

                if (markerIndex === -1) {
                    console.warn(`Marker with place_id ${place_id} not found`);
                    return prevMarkers;
                }

                return [
                    ...prevMarkers.slice(0, markerIndex),
                    { ...prevMarkers[markerIndex], ...updatedMarker },
                    ...prevMarkers.slice(markerIndex + 1)
                ];
            });

            return response;
        } catch (error) {
            console.error('Error updating marker:', error);
            throw error;
        }
    }

    useEffect(() => {
        fetchMarkers();
    }, []);

    useEffect(() => {
        // Фільтрація маркерів при зміні фільтрів
        if (Object.values(filters).some(f => f)) {
            const filtered = markers.filter(marker => {
                const hasVisualImpairment = marker.facilities.some((facility) => {
                    return facility.disability_types.some((disabilityType) =>
                        disabilityType === DISABILITY_TYPE_VISUAL_IMPAIRMENT
                    );
                });
                const hasHearingImpairment = marker.facilities.some((facility) => {
                    return facility.disability_types.some((disabilityType) =>
                        disabilityType === DISABILITY_TYPE_HEARING_IMPAIRMENT
                    );
                });
                const hasMobilityImpairment = marker.facilities.some((facility) => {
                    return facility.disability_types.some((disabilityType) =>
                        disabilityType === DISABILITY_TYPE_MOBILITY_IMPAIRMENT
                    );
                });

                return (
                    (!filters.visualImpairment || hasVisualImpairment) &&
                    (!filters.hearingImpairment || hasHearingImpairment) &&
                    (!filters.mobilityImpairment || hasMobilityImpairment)
                );
            });
            setFilteredMarkers(filtered);
        } else {
            setFilteredMarkers(markers);
        }
    }, [filters, markers]);

    const handleFilterChange = (filter) => {
        setFilters(prev => ({
            ...prev,
            [filter]: !prev[filter]
        }));
    };

    const onMarkerClick = (marker) => {
        if (routeMode) {
            setFromPoint({
                lat: marker.location.latitude,
                lng: marker.location.longitude
            });
            setFromAddress(marker.address);
        } else {
            setSelectedMarker(marker);
            setIsMenuOpen(true);
        }
    }

    const onMapClick = async (e) => {
        console.log('onMapClick', e);

        const marker = e.detail.placeId
            ? markers.find((marker) => marker.place_id === e.detail.placeId)
            : null;

        if (routeMode) {
            setFromPoint(e.detail.latLng);
            setFromAddress(`${e.detail.latLng.lat.toFixed(6)}, ${e.detail.latLng.lng.toFixed(6)}`);
        } else if (marker) {
            setSelectedMarker(marker);
            setIsMenuOpen(true);
        }
    };

    const handleRouteSubmit = async (e) => {
        e.preventDefault();

        setIsLoadingRoute(true);

        try {
            const response = await getRoute({
                payload: {
                    origin: fromPoint,
                    destination: toPoint,
                }
            });

            if (response.status === 200) {
                const routeData = response.data.routes[0];
                const path = decodePolyline(routeData.overview_polyline.points);

                setRoute({
                    path,
                    start: routeData.legs[0].start_location,
                    end: routeData.legs[0].end_location
                });
            }
        } catch (error) {
            console.error('Error fetching directions:', error);
        } finally {
            setIsLoadingRoute(false);
        }
    };


    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <div className="app">
            <div className="app__map-container">
                <Map
                    className="app__map"
                    defaultCenter={{lat: 50.4501, lng: 30.5234}}
                    defaultZoom={12}
                    gestureHandling={'greedy'}
                    disableDefaultUI={true}
                    onClick={onMapClick}
                    mapId={GOOGLE_MAP_ID}
                >
                    {filteredMarkers.length > 0 && filteredMarkers.map((marker) => {
                        const isSelected = marker.place_id === selectedMarker?.place_id;
                        const isFromPoint = fromPoint &&
                            marker.location.latitude === fromPoint.lat &&
                            marker.location.longitude === fromPoint.lng;
                        const isToPoint = toPoint &&
                            marker.location.latitude === toPoint.lat &&
                            marker.location.longitude === toPoint.lng;

                        let backgroundColor, borderColor, glyphColor;

                        if (isFromPoint) {
                            backgroundColor = 'rgb(123,169,251)';
                            borderColor = 'rgb(57,130,253)';
                            glyphColor = 'rgb(74,137,250)';
                        } else if (isSelected) {
                            backgroundColor = 'rgb(253,213,131)';
                            borderColor = 'rgb(255,174,0)';
                            glyphColor = 'rgb(255,175,0)';
                        } else if (isToPoint) {
                            backgroundColor = 'rgb(52, 168, 83)';
                            borderColor = 'rgb(1,122,35)';
                            glyphColor = 'rgb(31,175,71)';
                        } else {
                            backgroundColor = 'rgb(234, 67, 53)';
                            borderColor = 'rgb(197, 34, 31)';
                            glyphColor = 'rgb(179, 20, 18)';
                        }

                        return (
                            <AdvancedMarker
                                position={{
                                    lat: marker.location.latitude,
                                    lng: marker.location.longitude,
                                }}
                                key={marker.place_id}
                                onClick={() => onMarkerClick(marker)}
                            >
                                <Pin
                                    background={backgroundColor}
                                    borderColor={borderColor}
                                    glyphColor={glyphColor}
                                />
                            </AdvancedMarker>
                        );
                    })}

                    {fromPoint && !markers.some(m =>
                        m.location.latitude === fromPoint.lat &&
                        m.location.longitude === fromPoint.lng
                    ) && (
                        <AdvancedMarker position={fromPoint}>
                            <Pin
                                background={'rgb(66, 133, 244)'}
                                borderColor={'rgb(56, 123, 234)'}
                                glyphColor={'white'}
                            />
                        </AdvancedMarker>
                    )}

                    {route && (
                        <>
                            <Polyline
                                path={route.path}
                                strokeColor="#4285F4"
                                strokeOpacity={1.0}
                                strokeWeight={4}
                            />
                        </>
                    )}
                </Map>
            </div>

            <button
                className={`app__filter-toggle ${isFilterOpen && 'app__filter-toggle--open'} ${isMenuOpen && 'filter-menu--shifted'}`}
                onClick={() => setIsFilterOpen(!isFilterOpen)}
            >
                Фільтри
            </button>
            <div
                className={`filter-menu ${isFilterOpen && 'filter-menu--open'} ${isMenuOpen && 'filter-menu--shifted'}`}>
                <div className="filter-options">
                    <label className="filter-option">
                        <input
                            type="checkbox"
                            checked={filters.visualImpairment}
                            onChange={() => handleFilterChange('visualImpairment')}
                        />
                        <span>Для людей з вадами зору</span>
                    </label>
                    <label className="filter-option">
                        <input
                            type="checkbox"
                            checked={filters.hearingImpairment}
                            onChange={() => handleFilterChange('hearingImpairment')}
                        />
                        <span>Для людей з вадами слуху</span>
                    </label>
                    <label className="filter-option">
                        <input
                            type="checkbox"
                            checked={filters.mobilityImpairment}
                            onChange={() => handleFilterChange('mobilityImpairment')}
                        />
                        <span>Для людей з обмеженими можливостями</span>
                    </label>
                </div>
            </div>

            <button
                className={`app__menu-toggle ${isMenuOpen ? 'app__menu-toggle--open' : ''}`}
                onClick={toggleMenu}
            >
                {isMenuOpen ? <FiChevronLeft size={20}/> : <FiChevronRight size={20}/>}
            </button>
            <SideMenu
                isOpen={isMenuOpen}
                selectedMarker={selectedMarker}
                onClose={() => setIsMenuOpen(false)}
                routeMode={routeMode}
                setRouteMode={setRouteMode}
                fromAddress={fromAddress}
                setFromPoint={setFromPoint}
                setFromAddress={setFromAddress}
                toAddress={toAddress}
                setToAddress={setToAddress}
                setToPoint={setToPoint}
                onSubmitRoute={handleRouteSubmit}
                isLoadingRoute={isLoadingRoute}
                refetchPlace={fetchMarker}
            />
        </div>
    );
}