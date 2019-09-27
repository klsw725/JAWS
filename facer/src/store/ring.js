const state = {
    ringState: false,
};

const getters = {
    ringState: (state, getters, rootState) => {
        return state.ringState
    }
};

const actions = {

};

const mutations = {
    showRing(state){
        state.ringState = true;
    },
    hideRing(state){
        state.ringState = false;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
