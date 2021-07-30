import {compose, withState, lifecycle} from 'recompose';


const withTimer = (timerTask, interval, timerIdName) => compose(
    withState(timerIdName, 'set' + timerIdName, -1),
    lifecycle({
        componentDidMount() {
            const intervalId = setInterval(() => timerTask(this.props), interval);
            this.props['set' + timerIdName](intervalId);
        },
        componentWillUnmount() {
            clearInterval(this.props[timerIdName]);
        },
    })
);

export default withTimer;
