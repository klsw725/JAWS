import axios from "axios";

const state = {
    logged: false,
};

const getters = {
    userinfo: (state, getters, rootState) => {
        return state.userinfo;
    },
};

const actions = {
    async signup({commit}, {upload, data}){
        let res = await axios.post(upload, data);
        return res;
    },
    async login({commit}, {upload, data}){
        let res = await axios.post(upload, data);
        commit('setLogged');
        return res;
    },
    async logout({comit}, {upload, token}){
        let res = await axios.post (upload, token, {
            headers: {
                'Authorization': `token ${token}`
            }
        });
        commit('disableLogged');
        return res;
    }
};

const mutations = {
    setLogged(state){
        state.logged = true;
    },
    disableLogged(state){
        state.logged = false;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
