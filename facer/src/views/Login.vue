<template>
    <div class="wrapper">
        <div class="form-signin" name="login">
            <h2 class="form-signin-heading">Please login</h2>
            <input type="text" class="form-control" v-model="id" placeholder="ID" required="" autofocus="" />
            <input type="password" class="form-control" v-model="pw" placeholder="Password" required=""/>
            <button class="btn btn-lg btn-primary btn-block" @click="loginForm">Login</button>
            <button class="btn btn-lg btn-primary btn-block" @click="moveToSignup()">Sign up</button>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: "Login",
        data() {
            return {
                id: '',
                pw:'',
            }
        },
        computed: {
            ...mapGetters({
                userinfo: 'user/userinfo'
            })
        },
        methods:{
            checkForm() {
                if(!this.id || !this.pw){
                    alert('ID와 PW를 모두 입력해주세요.');
                    return false;
                }
                return true;
            },
            moveToSignup() {
                this.$router.push('/signup')
                // window.location='/signup';
            },
            async loginForm(){
                if(this.checkForm()){
                    let data = new FormData();
                    data.append("username", this.id);
                    data.append("password", this.pw);

                    // let res = await this.$store.dispatch('user/login', {upload:'http://localhost:8000/api/login/', data: data})
                    let res = await this.$store.dispatch('user/login', {upload:'http://ddotmotion.kr:8881/api/login/', data: data})
                    if (res.status === 200) {
                        localStorage.setItem(
                            "userInfo",
                            JSON.stringify({
                                id: res.data.user.id,
                                username: res.data.user.username,
                                token: res.data.token
                            })
                        );
                        // this.$store.dispatch('user/getMe');
                        this.$router.push({name: 'upload'});
                    }
                    else if(res.stats==400){
                        alert(res.data.message);
                        window.location.href = '/';
                    }

                    // let res = await this.$store.dispatch('upload/upload', {upload: 'http://localhost:8000/api/signin/', data: data});
                    // window.location.href = '/upload';
                }
            }
        }
    }
</script>

<style scoped>
    body {
        background: #eee !important;
    }
    .wrapper {
        margin-top: 80px;
        margin-bottom: 80px;
    }
    .form-signin {
        max-width: 380px;
        padding: 15px 35px 45px;
        margin: 0 auto;
        background-color: #fff;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    .form-signin .form-signin-heading,
    .form-signin .checkbox {
        margin-bottom: 30px;
    }
    .form-signin .checkbox {
        font-weight: normal;
    }
    .form-signin .form-control {
        position: relative;
        font-size: 16px;
        height: auto;
        padding: 10px;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }
    .form-signin .form-control:focus {
        z-index: 2;
    }
    .form-signin input[type="text"] {
        margin-bottom: -1px;
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
    }
    .form-signin input[type="password"] {
        margin-bottom: 20px;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
    }
</style>