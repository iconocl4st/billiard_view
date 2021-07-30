
import Select from 'react-select';


const SELECT_STYLE = {
    position: 'absolute',
    top: 50,
    left: 0,
};

const WIDTH = 200;
const HEIGHT = 50;

const getStyle = (row, col) => ({
    position: 'absolute',
    top: row * HEIGHT,
    left: col < 0 ? 0 : (col * WIDTH),
    width: col < 0 ? '100%' : WIDTH,
    height: HEIGHT,
})

const GenerationFormView = ({
    generationType,
    generationTypes,
    setGenerationType,

    singleShotTypes,
    singleShotType,
    setSingleShotType,

    spotShotOptions,

}) => <div>
    <div style={getStyle(0, 0)}>
        Generation Type:
    </div>
    <div style={getStyle(0, 1)}>
        <Select options={generationTypes} onChange={({value}) => setGenerationType(value)}/>
    </div>
    <div style={getStyle(1, 0)}>
        Strictly All
    </div>
    <div style={getStyle(1, 1)}>
        <input disabled={generationType==='whole-table'} type={"checkbox"} />
    </div>
    <div style={getStyle(2, 0)}>
        Single Shot Generation:
    </div>
    <div style={getStyle(2, 1)}>
        <Select isDisabled={generationType!=='single-shots'} options={singleShotTypes} onChange={({value}) => setSingleShotType(value)}/>
    </div>
    <div style={getStyle(2, 2)}>
        Use wall shots
    </div>
    <div style={getStyle(2, 3)}>
        <input disabled={generationType!=='single-shots' || singleShotType!=='spot-shot'} type={"checkbox"} />
    </div>
    <div style={getStyle(2, 4)}>
        Practice Position
    </div>
    <div style={getStyle(2, 5)}>
        <input disabled={generationType!=='single-shots'} type={"checkbox"} />
    </div>
    <div style={getStyle(3, 0)}>
        From distribution
    </div>
    <div style={getStyle(3, 1)}>
        <Select
            options={[
                {label: 'uniform', value: 'Uniform'},
                {label: 'missed', value: 'From statistics'}]}
            onChange={({value}) => setGenerationType(value)}
            isDisabled={false}
        />
    </div>
</div>

export default GenerationFormView;
