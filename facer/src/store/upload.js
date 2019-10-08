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
    async getUpload({commit}, {upload, token}) {
        let res = null;
        try{
            res = await axios.get(upload,{
                headers: {
                    'Authorization': `token ${token}`
                }
            });
        }
        catch(error){
            res = error.response;
        }
        commit('setList', res.data.results);
    },
    async upload({commit}, {upload, data, token}){
        let res = null;
        try {
            res = await axios.post(upload, data, {
                headers: {
                    'Authorization': `token ${token}`
                }
            });
        }
        catch(error){
            res = error.response;
        }
        return res;
        // commit('addList', res);
    },
    async deleteUpload({commit}, {upload, token}){
        await axios.delete(upload, {
            headers: {
                'Authorization': `token ${token}`
            }
        });
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
