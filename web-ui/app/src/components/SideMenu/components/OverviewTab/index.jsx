import React, { useState } from "react";
import { FiEdit, FiCheck, FiX } from "react-icons/fi";
import Select from 'react-select';

const OverviewTab = ({ selectedMarker, availableFacilities, setFacilitiesForMarker }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [selectedFacilities, setSelectedFacilities] = useState([]);

    if (!selectedMarker) {
        return <></>;
    }

    const powerIndexPercent = selectedMarker.accessibility_rate * 100;

    const getMarkerColor = (percent) => {
        if (percent < 20) return '#ff0000';
        if (percent < 40) return '#ff8000';
        if (percent < 60) return '#ffff00';
        if (percent < 80) return '#80ff00';
        return '#00ff00';
    };

    const handleEditClick = () => {
        const currentFacilities = selectedMarker.facilities.map(f => ({
            value: f.facility_id,
            label: f.descriptive_name
        }));
        setSelectedFacilities(currentFacilities);
        setIsEditing(true);
    };

    const handleSave = async () => {
        const updatedFacilities = availableFacilities.filter((facility) =>
            selectedFacilities.some(
                (selectedFacility) => selectedFacility.value === facility.facility_id
            )
        );

        try {
            await setFacilitiesForMarker(selectedMarker.place_id, updatedFacilities);
            setIsEditing(false);
        } catch (error) {
            console.error("Помилка при збереженні зручностей:", error);
        }
    };

    const handleCancel = () => {
        setIsEditing(false);
    };

    const customStyles = {
        control: (provided) => ({
            ...provided,
            minHeight: '40px',
        }),
        menu: (provided) => ({
            ...provided,
            position: 'absolute',
            right: 0,
            width: 'auto',
            minWidth: '100%',
        }),
        menuPortal: (provided) => ({
            ...provided,
            zIndex: 9999,
        }),
        multiValue: (provided) => ({
            ...provided,
            maxWidth: '200px',
        }),
        multiValueLabel: (provided) => ({
            ...provided,
            whiteSpace: 'normal',
            wordBreak: 'break-word',
            maxWidth: '180px',
        }),
        option: (provided) => ({
            ...provided,
            whiteSpace: 'normal',
            wordBreak: 'break-word',
        }),
    };

    return (
        <div className="overview">
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

                    <div className="facilities-container">
                        <div className="facilities-list-container">
                            <div className="facilities-header">
                                <h4>Зручності</h4>
                                {!isEditing && (
                                    <button onClick={handleEditClick} className="edit-facilities-btn">
                                        <FiEdit size={16} />
                                    </button>
                                )}
                            </div>

                            {isEditing ? (
                                <Select
                                    isMulti
                                    options={availableFacilities.map((facility) => ({
                                        value: facility.facility_id,
                                        label: facility.descriptive_name,
                                    }))}
                                    value={selectedFacilities}
                                    onChange={setSelectedFacilities}
                                    className="facilities-select"
                                    classNamePrefix="select"
                                    placeholder="Оберіть зручності..."
                                    closeMenuOnSelect={false}
                                    styles={customStyles}
                                    menuPlacement="auto"
                                    menuPosition="fixed"
                                    menuShouldScrollIntoView={false}
                                />
                            ) : (
                                <ul className="power-data">
                                    {selectedMarker?.facilities?.map((facility) => (
                                        <li key={facility.facility_id} className="power-data__item">
                                            {facility.descriptive_name}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>

                        {isEditing && (
                            <div className="facilities-edit-actions">
                                <button onClick={handleSave} className="action-btn save-btn" title="Зберегти">
                                    <FiCheck size={18} />
                                </button>
                                <button onClick={handleCancel} className="action-btn cancel-btn" title="Скасувати">
                                    <FiX size={18} />
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OverviewTab;