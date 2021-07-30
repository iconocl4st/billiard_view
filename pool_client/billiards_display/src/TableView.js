import _ from 'lodash';
import {useEffect, useRef} from 'react';

import {createMapper, createRenderer, getDimensions} from './Renderer';
import {CONTROLS_STYLE, getControlStyle, TABLE_STYLE, TABLE_WIDTH_PERCENTAGE} from "./Cascades";

const callGetDimensions = (viewWidth, {width, height}, inset) => getDimensions({
    scaleFactor: 10,
    world: {
        minX: -inset, maxX: width + inset,
        minY: -inset, maxY: height + inset
    },
    viewWidth,
    invert: true
});

// sendShotSelection: async shot => {
// sendGetCuts: async () => {
// sendCuts: async cuts => {

const TableView = props => {
    const graphics = _.get(props, 'graphics', {graphics: []});
    const dimensions = _.get(props, 'dimensions');
    const sendGenerateBallLocations = _.get(props, 'sendGenerateBallLocations');
    const sendGetBallLocations = _.get(props, 'sendGetBallLocations');
    const sendGetShots = _.get(props, 'sendGetShots');
    const mouseMoveListener = _.get(props, 'mouseMoveListener');
    const mouseClickListener = _.get(props, 'mouseClickListener');
    const clearSelection = _.get(props, 'clearSelection');
    const sendRequestSpotShot = _.get(props, 'sendRequestSpotShot');
    const canvasRef = useRef(null);
    const viewWidth = TABLE_WIDTH_PERCENTAGE * window.innerWidth;
    const dims = callGetDimensions(viewWidth, dimensions.table, graphics.inset);
    const backgroundImage = new Image();
    backgroundImage.src = 'http://localhost:5000/image/';

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        const mapper = createMapper(dims);
        const g = createRenderer(context, mapper);
        context.drawImage(backgroundImage, 0, 0, context.canvas.width, context.canvas.height);
        g.setBackground(graphics.background);
        for (const graphic of graphics.graphics) {
            g.drawGraphics(graphic);
        }
    }, [viewWidth, dims, graphics, backgroundImage]);



    const mapper = createMapper(dims);
    return <div>
        <div style={CONTROLS_STYLE}>
            <button onClick={() => sendGenerateBallLocations()} style={getControlStyle(0, 5)}>
                Generate Random Ball Locations
            </button>
            <button onClick={() => sendGetBallLocations()} style={getControlStyle(1, 5)}>
                Update Ball Locations
            </button>
            <button onClick={() => sendGetShots()} style={getControlStyle(2, 5)}>
                Get Shots
            </button>
            <button onClick={() => clearSelection()}  style={getControlStyle(3, 5)}>
                Clear Selection
            </button>
            <button onClick={() => sendRequestSpotShot()}  style={getControlStyle(4, 5)}>
                Get Spot Shot
            </button>
        </div>
        <canvas
            onMouseMove={mouseMoveListener(canvasRef, mapper)}
            onMouseUp={mouseClickListener}
            ref={canvasRef}
            style={{...dims.viewDims, ...TABLE_STYLE}}
            width={dims.canvasDims.width} height={dims.canvasDims.height}
        />
    </div>;
};

export default TableView;
