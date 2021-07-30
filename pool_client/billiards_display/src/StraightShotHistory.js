import {compose, withState, withProps} from 'recompose';
import StraightShotHistoryView from './StraightShotHistoryView';


const StraightShotHistory = compose(
    withState('editing', 'setEditing', {row: -1, col: 0}),
    withState('currentRow', 'setCurrentRow', []),
    withState('shotType', 'setShotType', 'forward'),
    withProps({history: [
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0],
    ]}),
)(StraightShotHistoryView);

export default StraightShotHistory;