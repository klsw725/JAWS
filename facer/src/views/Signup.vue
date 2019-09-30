<template>
    <div class="wrapper">
        <div class="form-signin" name="signup">
            <h2 class="form-signin-heading">Sign Up</h2>
            <input type="text" class="form-control" v-model="code" placeholder="Device Code" required="" autofocus="" />
            <input type="text" class="form-control" v-model="id" placeholder="ID" required="" />
            <input type="password" class="form-control" v-model="pw" placeholder="Password" required=""/>
            <button class="btn btn-lg btn-primary btn-block" @click="signupForm">Submit</button>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Signup",
        data() {
            return {
                id: '',
                pw:'',
                code:'',
            }
        },
        created() {
            document.title = "JAWS SIGNUP";
        },
        methods:{
            checkForm() {
                if (!this.id || !this.pw || !this.code) {
                    alert('ID, PW, 기기코드를 모두 입력해주세요.');
                    return false;
                }
                return true;
            },
            async signupForm(){
                if(this.checkForm()){
                    let data = new FormData();

                    data.append("username", this.id);
                    data.append("password", this.pw);
                    data.append("devicecode", this.code);

                    let res = await this.$store.dispatch('user/signup', {upload:'http://localhost:8000/api/signup/', data: data})

                    if (res.status === 201) {
                        this.$router.push({name: 'login'});
                    }
                    // let res = await this.$store.dispatch('upload/upload', {upload: 'http://localhost:8000/api/signup/', data: data});
                    // window.location.href = '/';
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