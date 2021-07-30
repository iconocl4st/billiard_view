import COLORS from './ColorScheme';

// const ROW_HEIGHT = 50;

const getTdStyle = (r, c) => ({

});

const NUMPAD_0 = 96;
const NUMPAD_1 = 97;

const BINARY_UNSELECTED_STYLE = {
    border: '1px solid black',
    width: '100%',
    height: '25px',
};
const BINARY_SELECTED_STYLE = {
    ...BINARY_UNSELECTED_STYLE,
    border: '1px solid yellow'
};

const attemptListener = editor => ({keyCode}) => {
    if (keyCode === NUMPAD_0) {
        editor(0);
    } else if (keyCode === NUMPAD_1) {
        editor(1);
    }
};

const editCurrentRow = props => value => {
    const {currentRow, setCurrentRow, editing, setEditing} = props;
    const nextRow = currentRow.concat(value);

    if (nextRow.length < 3) {
        setCurrentRow(nextRow);
        setEditing({row: -1, col: editing.col + 1});
        return;
    }

    setCurrentRow([]);
    setEditing({row: -1, col: 0});
};

const editPreviousRow = props => value => {

}


const BinaryInput = props => {
    const {row, col, value, editing: {row: er, col: ec}, setEditing} = props;
    const selected = (er === row && ec === col);
    const style = selected ? BINARY_SELECTED_STYLE : BINARY_UNSELECTED_STYLE;
    const editor = row < 0 ? editCurrentRow(props) : editPreviousRow(props);
    return (
        <input
            style={style}
            onMouseUp={() => setEditing({row, col})}
            onKeyUp={selected ? attemptListener(editor): () => {}}
            value={value}
        />
    )
};

const StraightShotHistoryView = props => {
    const {history, currentRow} = props;
    return (
        <div style={{width: '100%'}}>
            <div style={{...COLORS.controls}}>
            </div>
            <table style={{width: '100%'}}>
                <tr>
                    {[0, 1, 2].map(idx => (
                        <td key={`to-edit-${idx}`}>
                            <BinaryInput
                                row={-1} col={idx}
                                value={idx < currentRow.length ? currentRow[idx] : undefined}
                                {...props}
                            />
                        </td>
                    ))}
                </tr>
                {(history || []).map((row, row_num) => (
                    <tr key={`history-row-${row_num}`}>
                        {(row || []).map((col, col_num) => (
                            <td key={`history-col-${row_num}-${col_num}`} style={getTdStyle(row_num, col)}>
                                <BinaryInput
                                    row={row_num} col={col_num}
                                    value={col}
                                    {...props}
                                />
                            </td>
                        ))}
                    </tr>
                ))}
            </table>
        </div>
    );
};

export default StraightShotHistoryView;
