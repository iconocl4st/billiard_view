import {compose, branch, renderNothing, withProps} from 'recompose';
import _ from 'lodash';
import ResetModalView from './ResetModalView';
import withTimer from "./Timer";
import { withReset } from './GoproClient';

const updateImage = props => {
    _.get(props, 'sendGetCurrentResetImage', ()=>{})();
};

const imageIdToPath = id => id ? ('http://localhost:5001/image/?id=' + id) : false;

const ResetModal = compose(
    branch(
        p => !_.get(p, 'open', false),
        renderNothing
    ),
    withReset,
    withTimer(updateImage, 1000, 'reset-timer'),
    withProps(props => ({
        originalImagePath: _.get(props, 'snapshot.url', false),
        currentImagePath: _.get(props, 'resetImage.image.url', false)
    })),
)(ResetModalView);

export default ResetModal;


