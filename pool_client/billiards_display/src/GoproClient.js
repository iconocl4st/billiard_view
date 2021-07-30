import axios from 'axios';
import {compose, withState, withProps, lifecycle} from 'recompose';

const shots_api = axios.create({
    baseURL: 'http://localhost:5001',
    timeout: 1000,
});


export const withSnapshots = compose(
    withState('snapshots', 'setSnapshots', []),
    withProps(({setSnapshots}) => ({
        sendGetSnapshots: async () => {
            try {
                const { data: {snapshots, success}, status } = await shots_api.get('/snapshots/');
                if (status === 200 && success) {
                    return setSnapshots(snapshots);
                }
            } catch (error) {
                console.error(error);
            }
        }
    })),
    withProps(({sendGetSnapshots}) => ({
        sendCreateSnapshot: async () => {
            try {
                const { data: { snapshot, success }, status } = await shots_api.put('/snapshots/');
                if (status === 200 && success) {
                    await sendGetSnapshots();
                }
            } catch (error) {
                console.error(error);
            }
        },
        sendRemoveSnapshot: async id => {
            try {
                const { data: {success}, status } = await shots_api.delete(
                    '/snapshots/',
                    {data: {id}}
                );
                if (status === 200 && success) {
                    await sendGetSnapshots();
                }
            } catch (error) {
                console.error(error);
            }
        }
    })),
    lifecycle({
        async componentDidMount() {
            await this.props.sendGetSnapshots();
        }
    }),
);

export const withReset = compose(
    withState('resetImage', 'setResetImage', {empty: true}),
    withProps(({resetImage, setResetImage}) => ({
        sendBeginReset: async () => {
            try {
                const { data: {success}, status } = await shots_api.put('/reset/');
                return status === 200 && success;
            } catch (error) {
                console.error(error);
            }
            return false;
        },
        sendEndReset: async () => {
            try {
                const { data: {success}, status } = await shots_api.delete('/reset/');
                if (status === 200 && success) {
                    setResetImage({empty: true});
                }
            } catch (error) {
                console.error(error);
            }
        },
        sendGetCurrentResetImage: async () => {
            try {
                const { data: {success, message, image}, status } = await shots_api.get('/reset/');
                console.log('reset image', success, message, image)
                if (status !== 200 || !success) {
                    return;
                }
                if (!resetImage.empty && resetImage.image && resetImage.image.id === image.id) {
                    return;
                }
                setResetImage({empty: false, image});
            } catch (error) {
                console.error(error);
            }
        },
    })),
    lifecycle({
        async componentDidMount() {
            const began = await this.props.sendBeginReset();
            // Do something with began...
        },
        async componentWillUnmount() {
            await this.props.sendEndReset();
        },
    })
);
