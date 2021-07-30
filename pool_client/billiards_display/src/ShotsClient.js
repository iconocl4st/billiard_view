import {compose, withState, withProps, lifecycle} from 'recompose';
import _ from 'lodash';

import axios from 'axios';

const shots_api = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 1000,
});


///////////////////////////////////////////////////////////////////////////////////////////////////
// BALLS AND SHOTS
///////////////////////////////////////////////////////////////////////////////////////////////////

export const withShotSelection = compose(
    withState('ballLocations', 'setBallLocations', []),
    withState('shots', 'setShots', []),
    withState('selectedShot', 'setSelectedShot', -1),
    withState('highlightedShot', 'setHighlightedShot', -1),
    withProps(() => ({
        sendShotSelection: async shot => {
            console.log('selecting shot', shot);
            // TODO: implement...

            // if (highlightedShot < 0) {
            //     return;
            // }
            // await setShotSelection(highlightedShot);
        }
    })),
    withProps(({setSelectedShot, shots}) => ({
        setSelectedShotByKey: key => {
            if (!shots) {
                return;
            }
            for (let i=0; i<shots.length; i++) {
                console.log('is-eq', i, key, shots[i]['key'], _.isEqual(key, shots[i]['key']))
                if (_.isEqual(key, shots[i]['key'])) {
                    setSelectedShot(i);
                    console.log('set to', i);
                    return;
                }
            }
            console.log('--------------------')
        },
    })),
    withProps(({setShots, setHighlightedShot, setSelectedShot,}) => ({
        sendGetShots: async () => {
            try {
                const { data: { shots, success }, status } = await shots_api.get('/shots/');
                if (status === 200 && success) {
                    setShots(shots);
                } else {
                    setShots([]);
                }
            } catch (error) {
                console.error(error);
            }
            setHighlightedShot(-1);
            setSelectedShot(-1);
        },
    })),
    withProps(({sendGetShots, setBallLocations}) => ({
        sendGetBallLocations: async () => {
            const { data: { locations, success }, status } = await shots_api.get('/balls/');
            if (status !== 200 || !success) {
                return
            }
            setBallLocations(locations);
            await sendGetShots();
        }
    })),
    withProps(({setBallLocations, sendGetBallLocations}) => ({
        sendGenerateBallLocations: async () => {
            try {
                const { data: {success}, status } = await shots_api.post('/balls/', {'generation-type': 'random'});
                if (status === 200 && success) {
                    await sendGetBallLocations();
                }
            } catch (error) {
                console.error(error);
                return false;
            }
        },
    })),
    lifecycle({
        async componentDidMount() {
            // ignored promise...
            // this.props.generateBallLocations();
            await this.props.sendGetBallLocations();
        }
    })
);


///////////////////////////////////////////////////////////////////////////////////////////////////
// TABLE DIMENSIONS
///////////////////////////////////////////////////////////////////////////////////////////////////

export const withTableDimensions = compose(
    withState('dimensions', 'setDimensions', { table: {width: 46, height: 92}}),
    withProps(({setDimensions}) => ({
        sendGetPoolDimensions: async () => {
            const { data: {success, dimensions}, status } = await shots_api.get('/dimensions/');
            if (status === 200 && success) {
                setDimensions(dimensions);
            }
        }
    })),
    lifecycle({
        async componentDidMount() {
            await this.props.sendGetPoolDimensions();
        }
    })
);

///////////////////////////////////////////////////////////////////////////////////////////////////
// CUTS
///////////////////////////////////////////////////////////////////////////////////////////////////

export const withCuts = compose(
    withState('cuts', 'setCuts', []),
    withProps(({setCuts}) => ({
        sendGetCuts: async () => {
            try {
                const { data: {cuts, success}, status } = await shots_api.get('/cuts/');
                if (status === 200 && success) {
                    setCuts(cuts);
                }
            } catch (error) {
                console.error(error);
            }
        }
    })),
    lifecycle({
        async componentDidMount() {
            await this.props.sendGetCuts();
        }
    })
);

export const withSendCuts = withProps({
    sendCuts: async cuts => {
        try {
            const { data, status } = await shots_api.post('/cuts/', {cuts});
            return status === 200 && data.status === 'success';
        } catch (error) {
            console.error(error);
            return false;
        }
    }
});

export const withPractice = withProps(({
    sendGetBallLocations, setSelectedShotByKey
}) => ({
    sendRequestSpotShot: async () => {
        const requestData = {
            'params': {
                'generation-type': 'single-shot',
                'single-shot-type': 'spot-shot',
                'include-walls': false,
                'practice-position': false,
                'distribution': 'uniform',
            }
        };
        const { data, status } = await shots_api.post('/practice/', requestData);
        if (status !== 200 || !data.success) {
            return;
        }

        await sendGetBallLocations();
        setSelectedShotByKey(data['shot-key']);
    },
}));
