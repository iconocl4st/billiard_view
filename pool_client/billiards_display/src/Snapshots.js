
import { compose, withState,  withProps } from 'recompose';
import SnapshotsView from './SnapshotsView';
import {withSnapshots} from './GoproClient';

export default compose(
    withSnapshots,
    withState('selectedSnapshot', 'setSelectedSnapshot', -1),
    withState('modalShowing', 'showModal', false),
    withProps(({setSelectedSnapshot}) => ({
        clearSelectedSnapshot: () => setSelectedSnapshot(-1),
    })),
    withProps(({sendGetSnapshots, selectedSnapshot, clearSelectedSnapshot}) => ({
        makeSnapshot: () => sendGetSnapshots(),
        removeSnapshot: index => {
            if (index === selectedSnapshot) {
                clearSelectedSnapshot();
            }
            sendGetSnapshots();
        }
    })),
)(SnapshotsView);
