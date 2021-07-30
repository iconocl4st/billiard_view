import _ from 'lodash';
import COLORS, {COLORS_ARRAY, listColors} from "./ColorScheme";
import ResetModal from './ResetModal';
import {CONTROLS_STYLE, getControlStyle} from "./Cascades";
import {withProps} from "recompose";

const computeStyles = (w, num) => {
    const snapshotHeight = 0.5 * 0.2 * w +20;
    const container = {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
    }
    const snapshotsList = {
        position: 'absolute',
        left: 0,
        top: 50,
        height: num * snapshotHeight,
        width: '100%',
    };
    const snapshot = {
        position: 'absolute',
        border: '1px solid white',
        left: 0,
        width: '100%',
        height: snapshotHeight,
    };
    return {
        snapshotHeight,
        container,
        snapshotsList,
        snapshot
    };
};


const getTableStyle = idx => _.omit(getControlStyle(idx, 5), ['top', 'height']);

const Snapshot = ({date, url, id, selector, remover}) => (
    <div>
        <span style={getTableStyle(0)}>
            {date.toLocaleString()}
        </span>
        <span style={getTableStyle(1)}>
            <img alt='preview' style={{maxWidth: '100%', height: 'auto'}} src={url}/>
        </span>
        <span style={getTableStyle(2)}>
            {id}
        </span>
        <span style={getTableStyle(3)}>
            <button  style={{width: '100%'}} onClick={selector}>Select</button>
        </span>
        <span style={getTableStyle(4)}>
            <button  style={{width: '100%'}} onClick={remover}>Remove</button>
        </span>
    </div>
);

const SnapshotHeader = () => (
    <div>
        <span style={getTableStyle(0)}>Date</span>
        <span style={getTableStyle(1)}>Image</span>
        <span style={getTableStyle(2)}>Id</span>
    </div>
);

const GoProStatus = ({status}) => (
    <div style={{
        ...{connected: COLORS.good, disconnected: COLORS.bad}[status]
    }}>
        GoPro Status: {status}
    </div>
)


const SnapshotsView = props => {
    const snapshots = _.get(props, 'snapshots', []);
    const selectedSnapshotIndex = _.get(props, 'selectedSnapshot', -1);
    const setSelectedSnapshot = _.get(props, 'setSelectedSnapshot', ()=>{});
    const hasSelectedSnapshot = snapshots && selectedSnapshotIndex >= 0 && selectedSnapshotIndex < snapshots.length;
    const makeSnapshot = _.get(props, 'sendCreateSnapshot', () => {});
    const removeSnapshot = _.get(props, 'sendRemoveSnapshot', () => {});
    const modalShowing = _.get(props, 'modalShowing', false);
    const showModal = _.get(props, 'showModal', () => {});
    const status = _.get(props, 'gopro-status', 'disconnected');
    const styles = computeStyles(window.innerWidth, snapshots.length);

    return <div style={styles.container}>
        <div style={CONTROLS_STYLE}>
            <span style={getControlStyle(0, 5)}>
                <GoProStatus status={status}/>
            </span>
            <span style={getControlStyle(1, 5)}>
                <button style={{width: '100%'}} disabled={modalShowing}>
                    Refresh
                </button>
            </span>
            <span style={getControlStyle(2, 5)}>
                <button onClick={makeSnapshot} disabled={modalShowing} style={{width: '100%'}}>
                    Make a snapshot
                </button>
            </span>
            <span style={getControlStyle(3, 5)}>
                <button onClick={() => showModal(true)} disabled={modalShowing || !hasSelectedSnapshot} style={{width: '100%'}}>
                    Start reset
                </button>
            </span>
            <span style={getControlStyle(4, 5)}>
                <button onClick={() => {}} disabled={modalShowing} style={{width: '100%'}}>\
                    Configure
                </button>
            </span>
        </div>
        <ResetModal
            open={modalShowing}
            snapshot={hasSelectedSnapshot ? snapshots[selectedSnapshotIndex] : undefined}
            closeModal={() => showModal(false)}
        />
        <div style={styles.snapshotsList}>
            <div
                style={{
                    ...styles.snapshot, height: 25, top: 0,
                    ...listColors(-1)
                }}
            >
                <SnapshotHeader />
            </div>

            {snapshots.map((snapshot, index) => (
                <div
                    key={`snapshot-${index}`}
                    style={{
                        ...styles.snapshot,
                        ...listColors(index, selectedSnapshotIndex),
                        top: 25 + index * styles.snapshotHeight
                    }}
                >
                    <Snapshot
                        selector={() => setSelectedSnapshot(index)}
                        remover={() => removeSnapshot(index)}
                        {...snapshot}
                    />
                </div>
            ))}
        </div>
    </div>
};

export default SnapshotsView;
