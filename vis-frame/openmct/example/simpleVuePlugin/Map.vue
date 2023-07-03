
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
        <!-- <MglMarker :coordinates="coordinates" color="blue" /> -->
        <!-- <MglGeojsonLayer
        :sourceId="geoJsonSource.data.id"
        :source="geoJsonSource"
        layerId="somethingSomething"
        :layer="geoJsonLayer"
      /> -->

        <MglMarker
            :key="aircraftMarker"
            :coordinates="coordinates"
            :rotate-plane="rotateFctn"
        >
            <template slot="marker">
                <span>
                    <img
                        :style="'transform:rotate(' + rotateFctn + 'deg);'"
                        src="./plane.png"
                        width="25"
                        height="25"
                    >
                </span>
            </template>

        </MglMarker>

    </MglMap>
</div>
</template>

<script>
import Mapbox from "mapbox-gl";

import {MglMap, MglMarker, MglNavigationControl, MglGeojsonLayer } from "vue-mapbox";

export default {
    components: {
        MglMap,
        MglMarker,
        MglGeojsonLayer
    },
    data() {
        return {
            accessToken: 'pk.eyJ1IjoidHRvIiwiYSI6ImNqc3dkMzF2dTA5MnQ0M29maDQ3YTQyMmUifQ.ovQV_NNwcJ2DJwy8SwmveA', // your access token. Needed if you using Mapbox maps
            mapStyle: "mapbox://styles/mapbox/outdoors-v11", // your map style
            map: {},
            coordinates: [11.286146, 48.082427],
            aircraftMarker: "aircraft",
            rotatePlane: "0"

        };
    },
    computed: {
    // a computed getter
        reversedMessage: function () {
            // `this` points to the vm instance
            return this.message.split('').reverse().join('');
        },
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
            var Ac = document.getElementById('icon');

            // in component
            if (this.load === null) {
                this.load = event.map; // store the map object in here...
            }
            // or just to store if you want have access from other components
            //this.$store.map = event.map;

            mapDiv.style.width = '100%';
            mapCanvas.style.width = '100%';
            var canvasHeight = mapDiv.clientHeight - 50;
            mapCanvas.style.height = canvasHeight.toString() + 'px';

            this.load.resize();

            console.log(this.load);

            //console.log(mapDiv.clientHeight.toString()+'px')
        }
    }

};
</script>

<style scoped>
.marker {
  background-image: url('/plane.png');
  background-size: cover;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
}
</style>
