const state = {
    isOpen: false,
};

const getters = {
    isOpen: (state, getters, rootState) => {
        return state.isOpen;
    },
};

const actions = {

};

const mutations = {
    setOpen(state){
        state.isOpen = true;
    },
    setClose(state){
        state.isOpen = false;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
