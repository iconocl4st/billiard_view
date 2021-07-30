
import {compose, withState, withProps} from 'recompose';
import GenerationFormView from './GenerationFormView';

export default compose(
    withState('generationType', 'setGenerationType', ''),
    withState('singleShotType', 'setSingleShotType', ''),
    withProps({
        generationTypes: [{
            value: 'whole-table', label: 'All the balls'
        }, {
            value: 'single-shots', label: 'One shot at a time'
        }],
        singleShotTypes: [{
            value: 'spot-shot', label: 'Spot shots'
        }, {
            value: 'uniform', label: 'Uniform'
        }],
        spotShotOptions: []
    })
)(GenerationFormView);
