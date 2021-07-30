
export const COLORS_ARRAY = [
    'rgb(51, 92, 67)',
    'rgb(255, 243, 176)',
    'rgb(224, 159, 62)',
    'rgb(158, 42, 43)',
    'rgb(84, 11, 14)',
];

const COLORS = {
    background: { background: COLORS_ARRAY[1], color: COLORS_ARRAY[4] },

    unselectedTab: { background: COLORS_ARRAY[0], color: COLORS_ARRAY[1] },
    selectedTab: { background: COLORS_ARRAY[1], color: COLORS_ARRAY[4] },

    oddListElement: { background: COLORS_ARRAY[3], color: COLORS_ARRAY[1] },
    evenListElement: { background: COLORS_ARRAY[0], color: COLORS_ARRAY[1] },
    selectedListElement: { background: COLORS_ARRAY[1], color: COLORS_ARRAY[3] },

    good: { background: COLORS_ARRAY[0], color: COLORS_ARRAY[3] },
    bad: { background: COLORS_ARRAY[3], color: COLORS_ARRAY[1] },

    controls: { background: COLORS_ARRAY[4], color: COLORS_ARRAY[2], height: 50, width: '100%'},
};

export const listColors = (index, selectedIdx) => {
    if (index === selectedIdx) {
        return COLORS.selectedListElement;
    }
    if (index % 2 === 0) {
        return COLORS.evenListElement;
    }
    return COLORS.oddListElement;
};

export default COLORS;
