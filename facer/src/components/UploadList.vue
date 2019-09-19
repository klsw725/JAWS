<template>
    <div>
        <li v-for="index in list">
            {{index.name}}
            <img :src="index.image">
            <button class="delete" type="button" @click="deleteUpload(index.id)">Delete</button>
        </li>
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
                await this.$store.dispatch('upload/getUpload', `/api/upload`)
            },
            async deleteUpload(pk){
                await this.$store.dispatch('upload/deleteUpload', `/api/upload/${pk}`)
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

</style>