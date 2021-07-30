import { useRef, useEffect } from 'react';

import {createRenderer, getDimensions, createMapper, BLACK, WHITE} from './Renderer';
import COLORS from "./ColorScheme";
import {CONTROLS_STYLE, CUTS_STYLE, getControlStyle} from "./Cascades";

const drawCuts = (g, cuts) => {
    g.setBackground(BLACK);
    g.fillCircle({x: 0, y: 0, r: 1}, {color: WHITE})

    // TODO: create min x in mapper...
    for (const cut of cuts) {
        g.drawLine(
            [{x: cut, y: -1}, {x: cut, y: 1}],
            {color: {r: 255, g: 0, b: 0}, width: 3}
        );
    }
};

const CutsView = ({cuts, sendGetCuts})  => {
    const canvasRef = useRef(null);
    const viewWidth = 0.9 * window.innerWidth;

    const dimensions = getDimensions({
        scaleFactor: 1,
        world: {minX: -2, maxX: 2, minY: -1, maxY: 1},
        viewWidth,
        invert: false
    });

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        const mapper = createMapper(dimensions);
        const g = createRenderer(context, mapper);
        drawCuts(g, cuts || []);
    }, [cuts, viewWidth, dimensions]);

    return <div>
        <div style={CONTROLS_STYLE}>
            <button onClick={() => sendGetCuts()} style={getControlStyle(1, 3)}>
                Update Shot Selection
            </button>
        </div>
        <div style={{
            position: 'absolute',
            top: 50,
            height: 50,
            width: '100%',
            fontSize: 40,
            ...COLORS.background,
        }}>
            {cuts.map((cut, idx) => <span style={{
                ...getControlStyle(idx, cuts.length),
                top: 0,
                height: '100%',
                textAlign: 'center',
            }}>{cut.toFixed(3)}</span>)}
        </div>
        <canvas
            ref={canvasRef}
            style={{...dimensions.viewDims, ...CUTS_STYLE}}
            width={dimensions.canvasDims.width} height={dimensions.canvasDims.height}
        />
    </div>;
};

export default CutsView;