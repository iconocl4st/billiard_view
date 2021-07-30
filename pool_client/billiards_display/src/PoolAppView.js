import Cuts from "./Cuts";
import Table from "./Table";
import Snapshots from "./Snapshots";
import StraightShotHistory from './StraightShotHistory';
import GenerationForm from './GenerationForm';
import COLORS from "./ColorScheme";
import {getTabLabelStyle, TAB_STYLE} from "./Cascades";
import CheckerBoard from "./CheckerBoard";


const TABS = [
    ['table-view', 'Table View'],
    ['cut-view', 'Cut View'],
    ['straight-shot-view', 'Straight Shot View'],
    ['reset-view', 'Reset View'],
    ['practice-spots', 'Practice Spot Shots'],
    ['checker-board', 'Checkerboard']
];


const PoolAppView = ({ currentTab, setTab, ...props }) => (
    <div>
        <div style={{position: 'fixed', width: '100%', height: '100%', ...COLORS.background}} />
        <div>
            { TABS.map(([tabName, tabLabel], index) =>
                <div
                    key={`tab-label-${index}`}
                    style={getTabLabelStyle(TABS.length, index, currentTab === tabName)}
                    onClick={() => setTab(tabName)}
                >
                    <span style={{margin: 'auto'}}>{tabLabel}</span>
                </div>
            )}
        </div>
        <div>
            { currentTab === 'none' && (
                <div style={TAB_STYLE} />
            )}
            { currentTab === 'table-view' &&
                <div style={TAB_STYLE}><Table/></div>
            }
            { currentTab === 'cut-view' &&
                <div style={TAB_STYLE}><Cuts/></div>
            }
            { currentTab === 'straight-shot-view' &&
                <div style={TAB_STYLE}><StraightShotHistory/></div>
            }
            { currentTab === 'reset-view' &&
                <div style={TAB_STYLE}><Snapshots/></div>
            }
            { currentTab === 'practice-spots' &&
                <div style={TAB_STYLE}><GenerationForm/></div>
            }
            { currentTab === 'checker-board' &&
                <div style={TAB_STYLE}><CheckerBoard/></div>
            }
        </div>
    </div>
);

export default PoolAppView;
