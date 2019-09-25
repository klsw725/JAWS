import axios from "axios";

const state = {
    list: [],
    ringState: false,
};

const getters = {
    list: (state, getters, rootState) => {
        return state.list;
    },
    ringState: (state, getters, rootState) => {
        return state.ringState
    }
};

const actions = {
    async getUpload({commit}, upload) {
        let res = await axios.get(upload);
        commit('setList',res.data);
    },
    async upload({commit}, {upload, data}){
        console.log(data);
        let res = await axios.post(upload,data);
        console.log(res);
        commit('addList', res);
    },
    async deleteUpload({commit}, upload ){
        await axios.delete(upload);
        commit('deleteList');
    }
};

const mutations = {
    setList(state, data){
        state.list = data;
    },
    deleteList(state){
      // state.list.pop();
    },
    addList(state, data){
      // state.list.push(data);
    },
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
