import COLORS, {COLORS_ARRAY} from './ColorScheme';
import _ from 'lodash';
import {CONTROLS_STYLE, getControlStyle} from "./Cascades";

const MARGIN_PERCENTAGE = 3;

const IMAGE_STYLE= {
    position: 'absolute',
    top: 50,
    left: 0,
    width: '75%',
    height: 'auto',
};

const ResetModalView = ({snapshot, closeModal, originalImagePath, currentImagePath}) => <div>
    <div
        style={{
            ...COLORS.background,
            background: 'white',
            position: 'fixed',
            left: MARGIN_PERCENTAGE + '%',
            width: (100 - 2 * MARGIN_PERCENTAGE) + '%',
            top: MARGIN_PERCENTAGE + '%',
            height: (100 - 2 * MARGIN_PERCENTAGE) + '%',
            boxShadow: '0 0 2rem 2rem rgba(0, 0, 0, 0.5)',
            border: '1px solid ' + COLORS_ARRAY[4],
            zIndex: 10,
        }}
    >
        {/*{position: 'absolute', ...COLORS.controls, display: 'flex', justifyContent: 'center'}*/}
        <div style={CONTROLS_STYLE}>
            <button onClick={closeModal} style={getControlStyle(1, 3)}>
                Reset complete
            </button>
        </div>
        {originalImagePath && <img style={{...IMAGE_STYLE, zIndex: 10}} alt={'original'} src={originalImagePath} />}
        {currentImagePath && <img style={{...IMAGE_STYLE, zIndex: 11, opacity: 0.4}} alt={'current'} src={currentImagePath} />}
    </div>
</div>;

export default ResetModalView;
