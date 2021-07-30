

export const WHITE = {r: 255, g: 255, b: 255 };

export const BLACK = {r: 0, g: 0, b: 0};

export const createColor = ({r, g, b}) => ('rgba(' + r + ',' + g + ',' + b + ', 0.9)');

const mapVal = (x, origMinX, origMaxX, width) => width * (x - origMinX) / (origMaxX - origMinX);
// const getInverter = invert => !!invert ? (({x: y, y: x}) => ({x, y})) : (x => x);

export const getDimensions = ({
    scaleFactor: scaleFactorOption,
    world,
    viewWidth,
    invert
}) => {
    const scaleFactor = !!scaleFactorOption ? scaleFactorOption : 1.0;
    const {minX, minY, maxX, maxY} = world;
    const worldWidth = maxX - minX;
    const worldHeight = maxY - minY;
    // const scale = scaleFactor * viewWidth / ((!!invert ? worldWidth : worldHeight) + 2 * inset);
    const aspect = !!invert ? (worldWidth / worldHeight) : (worldHeight / worldWidth);
    const scale = scaleFactor * viewWidth / (!!invert ? worldHeight : worldWidth);
    const viewDims = {
        width: viewWidth,
        height: viewWidth * aspect
    };
    const canvasDims = {
        width: scaleFactor * viewDims.width,
        height: scaleFactor * viewDims.height,
    };
    return {scaleFactor, invert, world, viewDims, canvasDims, scale};
};

export const createMapper = dimensions => {
    const {scale, invert, world: {minX, minY, maxX, maxY}, canvasDims} = dimensions;
    return {
        scale,
        canvasToWorld: !!invert ? (
            ({x, y}) => {
                // console.log('try to map', ({x, y}));
                // console.log('found', {
                //     x: minX + (maxX - minX) * y / canvasDims.height,
                //     y: minY + (maxY - minY) * x / canvasDims.width,
                // })
                return ({
                    x: minX + (maxX - minX) * y / canvasDims.height,
                    y: minY + (maxY - minY) * x / canvasDims.width,
            }); }
        ) : (
            () => {}
        ),
        worldToCanvas: !!invert ? (
            ({x, y}) => ({
                x: mapVal(y, minY, maxY, canvasDims.width),
                y: mapVal(x, minX, maxX, canvasDims.height),
            })
        ) : (
            ({x, y}) => ({
                x: mapVal(x, minX, maxX, canvasDims.width),
                y: mapVal(y, minY, maxY, canvasDims.height),
            })
        ),
    };
};

export const createRenderer = (ctx, mapper) => {
    const setBackground = color => {
        ctx.fillStyle = createColor(color);
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    };
    const drawLine = ([p1, ...rest], {color, width}) => {
        const oldLineWidth = ctx.lineWidth;
        ctx.lineWidth = width;
        ctx.strokeStyle = createColor(color);
        ctx.beginPath();
        const {x: x1, y: y1} = mapper.worldToCanvas(p1);
        ctx.moveTo(x1, y1);
        for (const point of rest) {
            const {x: x2, y: y2} = mapper.worldToCanvas(point);
            ctx.lineTo(x2, y2);
        }
        ctx.stroke();
        ctx.lineWidth = oldLineWidth;
    };
    const fillCircle = ({x, y, r}, {color}) => {
        const {x: tx, y: ty} = mapper.worldToCanvas({x, y});
        ctx.fillStyle = createColor(color);
        ctx.beginPath();
        ctx.arc(tx, ty, mapper.scale * r, 0, 2 * Math.PI);
        ctx.closePath();
        ctx.fill();
    };
    const drawText = ({x, y, label}, {color}) => {
        ctx.fillStyle = createColor(color);
        ctx.font = 1 * mapper.scale + 'px Arial';
        ctx.textAlign = 'center';
        const {x: tx, y: ty} = mapper.worldToCanvas({x: x + 0.25, y});
        ctx.fillText(label, tx, ty);
    };
    const fillPolygon = ([p1, ...rest], {color}) => {
        ctx.fillStyle = createColor(color);
        ctx.beginPath();
        const {x: x1, y: y1} = mapper.worldToCanvas(p1);
        ctx.moveTo(x1, y1);
        for (const point of rest) {
            const {x: x2, y: y2} = mapper.worldToCanvas(point);
            ctx.lineTo(x2, y2);
        }
        ctx.lineTo(x1, y1);
        ctx.closePath();
        ctx.fill();
    };
    const fillArc = ({x, y, a1, a2, r}, {color}) => {
        const {x: cx, y: cy} = mapper.worldToCanvas({x, y});
         ctx.fillStyle = createColor(color);
         ctx.beginPath();
         ctx.arc(cx, cy, mapper.scale * r, a1, a2);
         ctx.closePath();
         ctx.fill();
    };
    return {
        setBackground,
        drawLine,
        fillCircle,
        drawText,
        fillPolygon,
        // fillRect: ([p1, p2], {color}),
        drawGraphics: ({type, params, options}) => {
            switch (type) {
                case 'circle':
                    if (!options.fill) {
                        throw Error("Not implemented");
                    }
                    fillCircle(params, options);
                    break;
                case 'line':
                    drawLine(params, options);
                    break;
                case 'text':
                    drawText(params, options);
                    break;
                case 'polygon':
                    if (!options.fill) {
                        throw Error("Not implemented");
                    }
                    fillPolygon(params, options);
                    break;
                case 'arc':
                    if (!options.fill) {
                        throw Error("Not implemented");
                    }
                    fillArc(params, options);
                    break;
                case 'none':
                    break;
                default:
                    throw Error('Unrecognized graphics: ' + type);
            }
        },
    };
}

