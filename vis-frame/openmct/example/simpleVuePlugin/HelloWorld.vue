
<template>
<!-- <div class="example">{{ msg }}</div> -->
<div id="root">
    <div id="example"
         class="example"
    >
        <p>Original message: "{{ message }}"</p>
        <p>Computed reversed message: "{{ reversedMessage }}"</p>
        Test
    </div>
    <div id="map"
         :style="{height: '100%' }"
    >
        <GmapMap
            :center="{lat:10, lng:10}"
            :zoom="7"
            map-type-id="terrain"
            style="width: 500px; height: 300px"
        >
            <GmapMarker
                v-for="(m, index) in markers"
                :key="index"
                :position="m.position"
                :clickable="true"
                :draggable="true"
                @click="center=m.position"
            />

        </GmapMap>
    </div>
</div>

</template>

<script>
//import * as VueGoogleMaps from 'vue2-google-maps'
import Vue2 from 'vue';

// Vue2.use(VueGoogleMaps, {
//     load: {
//         key: 'AIzaSyAjxxQnLT-aN7qBed0GS9a82rupwYJg-5g',
//         //v: '3.',
//         libraries: 'places', //// If you need to use place input

//     },
//     installComponents: true
// });

export default {
    data: function () {
        return {
            message: '',
            center: {
                lat: 10.0,
                lng: 10.0
            },
            markers: [{
                position: {
                    lat: 10.0,
                    lng: 10.0
                }
            }, {
                position: {
                    lat: 11.0,
                    lng: 11.0
                }
            }]
        };
    },
    computed: {
    // a computed getter
        reversedMessage: function () {
            // `this` points to the vm instance
            return this.message.split('').reverse().join('');
        }
    }
};
</script>

<style scoped>
.example {
  color: red !important;
  };
.vue-map-container {
    width: 100% !important;
    height:100% !important;
    };
    .vue-map-container {
    width: 100% !important;
    height:100% !important;
    };
    .vue-map {
    width: 100% !important;
    height:300px !important;
    };
</style>
