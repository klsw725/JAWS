<template>
    <div>
        <nav class="navbar navbar-expand-md navbar-dark bg-dark static-top">
            <div class="container">
                <a class="navbar-brand" href="/upload">Welcome {{this.user}}</a>
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item">
                            <button class="nav-link btn btn-link" @click="logoutForm">Logout</button>
                        </li>
                        <li class="nav-item active">
                            <a class="nav-link" href="/upload">Admin
                                <span class="sr-only">(current)</span>
                            </a>
                        </li>
                    </ul>
            </div>
        </nav>
    </div>
</template>

<script>
    export default {
        name: "Navigation",
        data(){
            return{
                user:''
            }
        },
        created(){
            this.user = localStorage.getItem("userInfo") ? JSON.parse(localStorage.getItem("userInfo")).username : null;
        },
        methods:{
            async logoutForm(){
                let token = localStorage.getItem("userInfo") ? JSON.parse(localStorage.getItem("userInfo")).token : null;
                let res = this.$store.dispatch('user/logout',{upload:'http://localhost:8000/api/logout/', token:token});
                console.log(res);
                localStorage.removeItem('userInfo')
                this.$router.push({name: 'login'});
            }
        }
    }
</script>

<style scoped>

</style>