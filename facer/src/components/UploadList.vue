<template>
    <div>
        <table class="userlist">
            <li v-for="index in list">
                <tr>
                    <td class="username">{{index.name}}</td>
                    <td><img class="thumbnail" :src="index.image"></td>
                    <td><button class="delete" type="button" @click="deleteUpload(index.id)">Delete</button></td>
                </tr>
            </li>
        </table>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    export default {
        name: "UploadList",
        computed: {
            ...mapGetters({
                list: 'upload/list'
            })
        },
        created() {
            this.getUpload();
        },
        methods:{
            async getUpload(){
                await this.$store.dispatch('upload/getUpload', `http://localhost:8000/api/upload/`)
            },
            async deleteUpload(pk){
                await this.$store.dispatch('upload/deleteUpload', `http://localhost:8000/api/upload/${pk}`)
                window.location.href = '/';
                // try{
                //   let res = await this.$axios.delete('/api/upload/'+pk);
                // window.location.href = '/';
                // }
                // catch(error){
                //   console.log(error);
                // }
            }
        }
    }
</script>

<style scoped>
    .userlist{
        margin-left: 1%;
        margin-top: 1%;
    }
    .username{
        font-size: large;
    }
    .thumbnail{
        width: 70%;
        height: 70%;
    }
</style>