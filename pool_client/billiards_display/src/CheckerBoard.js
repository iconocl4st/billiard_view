import _ from 'lodash';
import {CONTROLS_STYLE, getControlStyle, TABLE_STYLE, TABLE_WIDTH_PERCENTAGE} from "./Cascades";
import {BLACK, createColor} from "./Renderer";
import {useEffect, useRef} from "react";



const NUM_COLS = 10;
const NUM_ROWS = 7;

const getCheckerBoardStyle = ({w, h}, {w: tw, h: th}) => ({
    position: 'absolute',
    top: (th - 25 - h) / 2,
    left: (tw - w) / 2,
    width: w,
    height: h
});

const drawCheckerBoard = (ctx, {w, h}) => {
    const r = w / NUM_COLS;
    ctx.fillStyle = 'rgb(0, 0, 0)';
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    ctx.fillStyle = 'rgb(255, 255, 255)';
    for (let row=0; row * r <= h; row++) {
        for (let col=0; col * r <= w; col++) {
            if ((row + col) % 2 === 0) {
                continue;
            }
            ctx.beginPath();
            ctx.moveTo(r * col, r * row);
            ctx.lineTo(r * (col + 1), r * row);
            ctx.lineTo(r * (col + 1), r * (row + 1));
            ctx.lineTo(r * col, r * (row + 1));
            ctx.lineTo(r * col, r * row);
            ctx.closePath();
            ctx.fill();
        }
    }
};

const getDims = (w, h, aspect) => h < aspect * w ? {w: h / aspect, h} : {w, h: aspect * w};

const CheckerBoard = () => {
    const canvasRef = useRef(null);
    const aspect = NUM_ROWS / NUM_COLS;

    const windowDims = {w: window.innerWidth, h: window.innerHeight};
    const factor = 0.9;
    const canvasDims = getDims(
        factor * windowDims.w,
        factor * windowDims.h,
        NUM_ROWS / NUM_COLS);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        drawCheckerBoard(context, canvasDims)
    }, [canvasDims]);

    return <canvas
            ref={canvasRef}
            style={getCheckerBoardStyle(canvasDims, windowDims)}
            width={canvasDims.w} height={canvasDims.h}
    />
};

export default CheckerBoard;
