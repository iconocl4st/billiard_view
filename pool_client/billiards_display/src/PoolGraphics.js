import {BLACK, WHITE} from "./Renderer";
import _ from 'lodash';

const generateSpotGraphics = (w, h, nr, nc) =>
    _.range(nr).map(i => _.range(nc).map(j => ({
        type: 'circle',
        params: {
            x: w * (j + 1) / (nc + 1),
            y: h * (i + 1) / (nr + 1),
            r: 0.25
        },
        options: {
            color: {r: 255, g: 255, b: 255},
            fill: true,
        }
    }))).flat();

const generatePocketVertexGraphics = pockets => (pockets || []).map(
    ({vertices}) => vertices.map(({x, y}) => ({
        type: 'circle',
        params: {x, y, r: 0.25},
        options: {
            color: {r: 194, g: 185, b: 35},
            fill: true,
        }
    }))
).flat();


const createBallGraphics = (color, ball, location) => {
    const {x, y} = location;
    const {label, r, type} = ball;
    const a = 0.55;
    return (x < 0 || y < 0) ? [] : [
        {type: 'circle', params: {x, y, r}, options: {color, fill: true}},
        ...(type !== 'stripe' ? [] : [
            {
                type: 'arc',
                params: {x, y, r, a1: -a * Math.PI / 2, a2: a * Math.PI / 2},
                options: {color: WHITE, fill: true}},
            {
                type: 'arc',
                params: {x, y, r, a1: Math.PI - a * Math.PI / 2, a2: Math.PI + a * Math.PI / 2},
                options: {color: WHITE, fill: true}}
        ]),
        {type: 'circle', params: {x, y, r: 0.6 * r}, options: {color: WHITE, fill: true}},
        ...(label === 'cue' ? [] : [
            {type: 'text', params: {x, y, label}, options: {color: BLACK}},
        ]),
    ];
}

const generateFeltSpots = (w, h) => {
    return [];
};

const generateBallsGraphics = ({balls: ball_dimensions}, ballLocations) =>
    (!ball_dimensions || !ballLocations || ballLocations.length === 0) ? [] : [
        {r: 255, g: 255, b: 255},
        {r: 255, g: 245, b: 64},
        {r: 43, g: 59, b: 179},
        {r: 255, g: 0, b: 0},
        {r: 26, g: 1, b: 94},
        {r: 255, g: 159, b: 41},
        {r: 9, g: 148, b: 30},
        {r: 255, g: 25, b: 98},
        {r: 0, g: 0, b: 0},
        {r: 255, g: 245, b: 64},
        {r: 43, g: 59, b: 179},
        {r: 255, g: 0, b: 0},
        {r: 26, g: 1, b: 94},
        {r: 255, g: 159, b: 41},
        {r: 9, g: 148, b: 30},
        {r: 255, g: 25, b: 98},
    ].map((color, index) => createBallGraphics(
        color,
        ball_dimensions[index],
        ballLocations[index]
    )).flat();

const generateFeltGraphics = (w, h) => [{
    type: 'polygon',
    params: [
        {x: 0, y: 0},
        {x: w, y: 0},
        {x: w, y: h},
        {x: 0, y: h},
    ],
    options: {color: {r: 10, g: 70, b: 25}, fill: true}
}];

const generatePocketHoleGraphics = (w, h) => [
    { x: 0, y:   0, r: 3.1},
    { x: 0, y: h/2, r: 2.6},
    { x: 0, y:   h, r: 3.1},
    { x: w, y:   0, r: 3.1},
    { x: w, y: h/2, r: 2.6},
    { x: w, y:   h, r: 3.1},
].map((params, index) => [{
    type: 'circle',
    params,
    options: {fill: true, color: {r: 0, g: 0, b: 0}}
}]);

const getShotColor = (index, selectedShot, highlightedShot) => {
    if (index === selectedShot) {
        return {r: 255, g: 255, b: 255};
    }
    if (index === highlightedShot) {
        return {r: 219, g: 255, b: 51};
    }
    return {r: 194, g: 35, b: 136};
}

const generateShotGraphics = (shots, selectedShot, highlightedShot) => (shots || []).map(
    ({points, paths}, index) => [
        ...((paths || []).map(params => ({
            type: 'line',
            params,
            options: {
                color: getShotColor(index, selectedShot, highlightedShot),
                width: 20
            }
        }))),
        ...((points || []).map(point => ({
            type: 'circle',
            params: {r: 0.25, ...point},
            options: {color: WHITE, fill: true}
        }))),
    ]
).flat();
// // 	segments.map(({vertices}) => fillPolygon(ctx, table_dims, vertices, {color}));


export const createTableGraphics = ({dimensions, ballLocations, shots, selectedShot, highlightedShot}) => {
    const {width: w, height: h} = dimensions.table;
    return {
        background: {r: 245, g: 130, b: 7},
        inset: 2.0,
        graphics: [
            ...generateFeltGraphics(w, h),
            ...generateSpotGraphics(w, h, 7, 3),
            ...generateFeltSpots(w, h),
            ...generatePocketHoleGraphics(w, h),
            ...generatePocketVertexGraphics(dimensions.pockets),
            ...generateShotGraphics(shots, selectedShot, highlightedShot),
            ...generateBallsGraphics(dimensions, ballLocations),
        ].flat(),
    };
};

