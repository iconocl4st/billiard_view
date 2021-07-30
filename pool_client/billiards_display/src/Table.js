
import {compose, lifecycle, withProps, withState} from 'recompose';
import TableView from './TableView';
import {createTableGraphics} from './PoolGraphics';
import {calculateNearestShot} from "./PoolCalculations";
import {withTableDimensions, withShotSelection, withSendCuts, withPractice} from "./ShotsClient";

const withMouseListener = withProps(
    ({shots, highlightedShot, setHighlightedShot, selectedShot, setSelectedShot, sendCuts}) => ({
        mouseMoveListener: (canvasRef, mapper) => ({clientX, clientY}) => {
            const canvas = canvasRef.current;
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const loc = {x: (clientX - rect.left) * scaleX, y: (clientY - rect.top) * scaleY};
            const coord = mapper.canvasToWorld(loc);
            const nearestShotIndex = calculateNearestShot(shots, coord);
            if (nearestShotIndex === highlightedShot) {
                return;
            }
            setHighlightedShot(nearestShotIndex);
        },
        mouseClickListener: async () => {
            if (!shots ||
                highlightedShot < 0 ||
                highlightedShot === selectedShot ||
                highlightedShot >= shots.length
            ) {
                return;
            }
            const {cuts} = shots[highlightedShot];
            setSelectedShot(highlightedShot);
            await sendCuts(cuts);
        }
    })
);


export default compose(
    withTableDimensions,
    withShotSelection,
    withSendCuts,
    withPractice,
    withMouseListener,
    withProps(props => ({graphics: createTableGraphics(props)})),
    withProps(({setSelectedShot, setHighlightedShot, sendCuts}) => ({
        clearSelection: async () => {
            setSelectedShot(-1);
            setHighlightedShot(-1);
            await sendCuts([]);
        }
    }))
)(TableView);
