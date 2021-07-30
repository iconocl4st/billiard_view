
import { compose, withState } from 'recompose';

import PoolAppView from "./PoolAppView";


const PoolApp = compose(
    withState('currentTab', 'setTab', 'none'),
)(PoolAppView);

export default PoolApp;
