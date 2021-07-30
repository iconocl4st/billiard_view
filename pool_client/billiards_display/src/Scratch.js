
const generatePockets = () => [
    { x:  0, y:  0, r:   4, vertex_offsets: [{x: 0, y: 1}, {x: 1, y: 0}]},
    { x:  0, y: 46, r: 2.5, vertex_offsets: [{x: 0, y: -1}, {x: 0, y: 1}]},
    { x:  0, y: 92, r:   4, vertex_offsets: [{x: 0, y: -1}, {x: 1, y: 0}]},
    { x: 46, y:  0, r:   4, vertex_offsets: [{x: 0, y: 1}, {x: -1, y: 0}]},
    { x: 46, y: 46, r: 2.5, vertex_offsets: [{x: 0, y: -1}, {x: 0, y: 1}]},
    { x: 46, y: 92, r:   4, vertex_offsets: [{x: 0, y: -1}, {x: -1, y: 0}]},
].map(({x, y, r, vertex_offsets}, num) => ({
    num, vertices: vertex_offsets.map(({x: vx, y: vy}) => ({x: x + r * vx, y: y + r * vy}))
}));

export const POOL_DIMENSIONS = {
    table: { width: 46, height: 92, },
    pockets: generatePockets(),
    balls: [
        'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid',
        'stripe', 'stripe', 'stripe', 'stripe', 'stripe', 'stripe', 'stripe',
    ].map((type, num) => (num === 0 ? {
        type, num, label: 'cue', r: 2.26 / 2,
    } : {
        type, num, label: '' + num, r: 2.26 / 2,
    })),
};

const generateBallLocations = ({ table: { width, height } , balls}) => balls.map(
    (ball, idx) => ((Math.random() > 0.3 || idx < 2) ? ({
        x: ball.r + (width - 2 * ball.r) * Math.random(),
        y: ball.r + (height - 2 * ball.r) * Math.random()
    }) : ({x: -1, y: -1}))
);

export const BALL_LOCATIONS = generateBallLocations(POOL_DIMENSIONS);





//
// const addShot = ({ ball_infos, ball_locations, pocket_infos, dimensions: { table: table_dims, balls: { default_radius: r }}}) => {
//     const shot_infos = [];
//     const cue = ball_infos[0];
//
//     for (const obj of ball_infos) {
//         if (obj.num === 0) {
//             continue;
//         }
//         if (obj.x < 0 || obj.y < 0) {
//             continue;
//         }
//         for (const pocket of pocket_infos) {
//             const shot = calculateShot(cue, obj, pocket);
//             if (!shotIsPossible(shot, ball_infos, table_dims)) {
//                 continue;
//             }
//             shot_infos.push(shot);
//         }
//     }
//
//     return {
//         shot_infos,
//         calculateNearestShot: mousePosition => {
//             let nearestDist = 0;
//             let nearestIndex = -1;
//             for (let i=0; i<shot_infos.length; i++) {
//                 const dist = getDistanceToShot(shot_infos[i], mousePosition);
//                 if (dist < nearestDist || nearestIndex < 0) {
//                     nearestDist = dist;
//                     nearestIndex = i;
//                 }
//             }
//             return nearestIndex;
//         }
//     };
// };























export const getBallLocations = async setBallLocations => {
    try {
    } catch (error) {
        console.error(error);
    }
};


export const getSelectedShot = async setSelectedShot => {
    try {
        const { data, status } = await shots_api.get('/shots/selected/');
        if (status === 200) {
            setSelectedShot(data['selected-shot']);
        }
    } catch (error) {
        console.error(error);
    }
}

export const sendShotSelection = async (shotIndex, setSelectedShot) => {
    try {
        const { status } = await shots_api.post('/shots/selected/', {'shot-index': shotIndex});
        if (status === 200) {
            await getSelectedShot(setSelectedShot);
        }
    } catch (error) {
        console.error(error);
    }
}








// withProps(({setShots, setBallLocations, setSelectedShot, setHighlightedShot}) => ({
//     clearHighlightedShot: () => {
//         setHighlightedShot(-1);
//     },
//     clearShotSelection: () => {
//         setHighlightedShot(-1);
//         setSelectedShot(-1);
//     },
//     clearShots: () => {
//         setHighlightedShot(-1);
//         setSelectedShot(-1);
//         setShots([]);
//     },
//     clearBalls: () => {
//         setHighlightedShot(-1);
//         setSelectedShot(-1);
//         setShots([]);
//         setBallLocations([]);
//     }
// })),
//     withProps(({clearShots, updateShotSelection}) => ({
//         clearShotsAndSelection: async () => {
//             if (clearShots) {
//                 await clearShots();
//             }
//             if (updateShotSelection) {
//                 await updateShotSelection();
//             }
//         }
//     })),
//
//
// export const withShotSelection = compose(
//     withProps(({setSelectedShot}) => ({
//         updateShotSelection: async () => {
//             await getSelectedShot(setSelectedShot);
//         },
//         setShotSelection: async index => {
//             await sendShotSelection(index, setSelectedShot)
//         },
//     })),
//     withProps(({setShotSelection}) => ({
//         clearShotSelection: async () => {
//             await setShotSelection(-1);
//         },
//     })),
//     lifecycle({
//         componentDidMount() {
//             // ignored promise...
//             // this.props.generateBallLocations();
//             this.props.updateShotSelection();
//         }
//     })
// );