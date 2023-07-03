
<template>

<div id="mapWrap"
     style="height:100%; width:100%;"
>
    <MglMap
        :access-token="accessToken"
        :map-style.sync="mapStyle"
        :center="coordinates"
        :zoom="12"
        @load="onMapLoaded"
    >

        <MglMarker
            :key="aircraftMarker"
            :coordinates="[lon,lat]"
        >
            <template slot="marker">
                <span>
                    <img
                        :style="'transform:rotate(' + rotateFctn + 'deg);'"
                        src="/example/Map/plane.png"
                        width="40"
                        height="40"
                    >
                </span>
            </template>

        </MglMarker>

    </MglMap>
</div>
</template>

<script>
import Mapbox from "mapbox-gl";

import {MglMap, MglMarker} from "vue-mapbox";

export default {
    components: {
        MglMap,
        MglMarker
    },
    data() {
        return {
            accessToken: 'pk.eyJ1IjoidHRvIiwiYSI6ImNqc3dkMzF2dTA5MnQ0M29maDQ3YTQyMmUifQ.ovQV_NNwcJ2DJwy8SwmveA', // your access token. Needed if you using Mapbox maps
            mapStyle: "mapbox://styles/mapbox/outdoors-v11", // your map style
            map: {},
            coordinates: [11.286146, 48.082427],
            rotatePlane: "0",
            aircraftMarker: "AC",
            lat: 48.082427,
            lon: 11.286146

        };
    },
    computed: {
    // a computed getter
        rotateFctn: function () {
        //console.log(this.rotatePlane)
            return this.rotatePlane;
        }
    },

    created() {
    // We need to set mapbox-gl library here in order to use it in template
        this.mapbox = Mapbox;
        this.load = null;
    },
    methods: {
        onMapLoaded(event) {
            var mapCanvas = document.getElementsByClassName('mapboxgl-canvas')[0];
            var mapDiv = document.getElementById('mapWrap');

            // in component
            if (this.load === null) {
                this.load = event.map; // store the map object in here...
            }
            // or just to store if you want have access from other components
            //this.$store.map = event.map;

            mapDiv.style.width = '100%';
            mapCanvas.style.width = '100%';
            var canvasHeight = mapDiv.clientHeight;
            mapCanvas.style.height = canvasHeight.toString() + 'px';

            this.load.resize();

            //console.log(this.load);

        }
    }

};
</script>

