import {useEffect, useRef} from 'react';
import {useMap} from '@vis.gl/react-google-maps';

export const Polyline = ({path, ...options}) => {
    const map = useMap();
    const polylineRef = useRef(null);

    useEffect(() => {
        if (!map) return;

        if (!polylineRef.current) {
            polylineRef.current = new window.google.maps.Polyline({
                map,
                path,
                ...options
            });
            console.log('after creating polyline');
        }

        return () => {
            if (polylineRef.current) {
                polylineRef.current.setMap(null);
                polylineRef.current = null;
            }
        };
    }, [map, options, path]);

    useEffect(() => {
        if (!polylineRef.current) return;
        polylineRef.current.setOptions(options);
    }, [options]);

    useEffect(() => {
        if (!polylineRef.current) return;
        polylineRef.current.setPath(path);
    }, [path]);

    return null;
};