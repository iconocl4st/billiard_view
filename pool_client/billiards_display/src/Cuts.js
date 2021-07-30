import { compose } from 'recompose';
import CutsView from './CutsView';
import {withCuts} from "./ShotsClient";
import withTimer from "./Timer";


const updateCuts = ({sendGetCuts}) => sendGetCuts();

const Cuts = compose(
    withCuts,
    withTimer(updateCuts, 1000, 'cutsUpdateId'),
)(CutsView);

export default Cuts;
