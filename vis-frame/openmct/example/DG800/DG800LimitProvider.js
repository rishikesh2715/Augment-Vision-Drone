/*****************************************************************************
 * Open MCT, Copyright (c) 2014-2020, United States Government
 * as represented by the Administrator of the National Aeronautics and Space
 * Administration. All rights reserved.
 *
 * Open MCT is licensed under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * Open MCT includes source code licensed under additional open source
 * licenses. See the Open Source Licenses file (LICENSES.md) included with
 * this source code distribution or the Licensing information page available
 * at runtime from the About dialog for additional information.
 *****************************************************************************/

define([

], function (

) {
    //set your limits HIGH -> upper limit; LOW -> lower limit, use keys also used in dictionary
    var RED_HIGH = {
            
        },
        RED_LOW = {
            'data.gps.gSpeed': 15,
            'data.gps.heightMS': 10
        },

        YELLOW_HIGH = {
            
        },
        YELLOW_LOW = {
            'data.gps.gSpeed': 25,
            'data.gps.heightMS': 20
        },
        
        LIMITS = {
            rh: {
                cssClass: "is-limit--upr is-limit--red",
                low: RED_HIGH,
                high: Number.POSITIVE_INFINITY,
                name: "Red High"
            },
            rl: {
                cssClass: "is-limit--lwr is-limit--red",
                high: RED_LOW,
                low: Number.NEGATIVE_INFINITY,
                name: "Red Low"
            },
            yh: {
                cssClass: "is-limit--upr is-limit--yellow",
                low: YELLOW_HIGH,
                high: RED_HIGH,
                name: "Yellow High"
            },
            yl: {
                cssClass: "is-limit--lwr is-limit--yellow",
                low: RED_LOW,
                high: YELLOW_LOW,
                name: "Yellow Low"
            }
        };
        

    function DG800LimitProvider() {

    }

    DG800LimitProvider.prototype.supportsLimits = function (domainObject) {
        return domainObject.type === 'DG800.telemetry';
    };

    DG800LimitProvider.prototype.getLimitEvaluator = function (domainObject) {
        return {
            evaluate: function (datum, valueMetadata) {
                var key = domainObject.identifier.key
                var value = valueMetadata && valueMetadata.key;
                                
                if (datum[value] > RED_HIGH[key]) {
                    return LIMITS.rh;
                }

                if (datum[value] < RED_LOW[key]) {
                    return LIMITS.rl;
                }

                if (datum[value] > YELLOW_HIGH[key]) {
                    return LIMITS.yh;
                }

                if (datum[value] < YELLOW_LOW[key]) {
                    return LIMITS.yl;
                }
            }
        };
    };

    return DG800LimitProvider;
});
