import COLORS from "./ColorScheme";

const TAB_LABEL_HEIGHT = 50;

export const getTabWidthPercentage = num_tabs => (100 / num_tabs) - 0.05;

export const TAB_STYLE = {
    position: 'absolute',
    top: TAB_LABEL_HEIGHT,
    left: 0,
    width: '100%',
};

export const getTabLabelStyle = (num_tabs, index, selected) => ({
    position: 'absolute',
    border: '1px solid white',
    textAlign: 'center',
    verticalAlign: 'center',
    width: getTabWidthPercentage(num_tabs) + '%',
    height: TAB_LABEL_HEIGHT,
    display: 'flex',

    left: (index * getTabWidthPercentage(num_tabs)) + '%',
    ...(selected ? COLORS.selectedTab : COLORS.unselectedTab)
});


export const TABLE_WIDTH_PERCENTAGE = 0.8;

export const CONTROLS_STYLE = {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: 50,
    ...COLORS.controls
};

export const getControlStyle = (idx, max) => ({
    position: 'absolute',
    left: (idx * 100 / max + 1) + '%',
    top: '25%',
    width: (100 / max - 2) + '%',
    height: '50%',
});

export const TABLE_STYLE = {
    position: 'absolute',
    left: ((1 - TABLE_WIDTH_PERCENTAGE) * 50) + '%',
    top: CONTROLS_STYLE.height,
};

export const CUTS_STYLE = {
    position: 'absolute',
    left: '5%',
    top: 100,
};
