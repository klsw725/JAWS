import axios from "axios";

const state = {
    list: [],
};

const getters = {
    list: (state, getters, rootState) => {
        return state.list;
    },
};

const actions = {
    async getUpload({commit}, upload) {
        let res = await axios.get(upload);
        commit('setList', res.data);
    },
    async upload({commit}, {upload, data}){
        let res = null;
        try {
            res = await axios.post(upload, data);
        }
        catch(error){
            console.log(error)
        }
        return res;
        // commit('addList', res);
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
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
