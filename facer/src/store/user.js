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
        let res = null;
        try {
            res = await axios.post(upload, data);
        }
        catch (error){
            res = error.response;
        }

        return res;
    },
    async login({commit}, {upload, data}){
        let res = null;
        try {
            res = await axios.post(upload, data);
            commit('setLogged');
        }
        catch(error){
            res = error.response;
        }
        return res;
    },
    async logout({commit}, {upload, token}){
        let res = null;
        try {
            res = await axios.post(upload, token, {
                headers: {
                    'Authorization': `token ${token}`
                }
            });
            commit('disableLogged');
        }
        catch(error){
            res = error.response;
        }
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
