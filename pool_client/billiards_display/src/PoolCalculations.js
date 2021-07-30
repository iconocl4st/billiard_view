
const TOLERANCE = 1e-12;

const subtract = (a, b) => ({x: a.x - b.x, y: a.y - b.y});

const dot2d = (a, b) => a.x * b.x + a.y * b.y;

const norm2 = p => dot2d(p, p);

const distance2 = (p1, p2) => norm2(subtract(p1, p2));

const distance = (p1, p2) => Math.sqrt(distance2(p1, p2));

const getDistanceToSegment = ([l1, l2], p) => {
    const nrm = distance2(l1, l2);
    if (nrm < TOLERANCE) {
        return distance(l1, p);
    }
    const t = Math.max(0, Math.min(1, dot2d(subtract(p, l1), subtract(l2, l1)) / nrm));
    const proj = {x: l1.x + t * (l2.x - l1.x), y: l1.y + t * (l2.y - l1.y)};
    return distance(proj, p);
};

const lineToSegments = line => {
    const ret = []
    for (let i=0; i<line.length - 1; i++) {
        ret.push([line[i], line[i+1]]);
    }
    return ret;
};

const getDistanceToShot = ({paths}, point) =>
    Math.min(...paths.map(line => Math.min(...lineToSegments(line).map(
        segment => getDistanceToSegment(segment, point)))));


export const calculateNearestShot = (shots, point) => {
    if (!shots) {
        return -1;
    }
    let nearestDist = 0;
    let nearestIndex = -1;
    for (let i=0; i<shots.length; i++) {
        const dist = getDistanceToShot(shots[i], point);
        if (dist < nearestDist || nearestIndex < 0) {
            nearestDist = dist;
            nearestIndex = i;
        }
    }
    return nearestIndex;
};