<template>
  <div>
    <h1>Upload new File</h1>
<!--    <form action="/">-->
      <p>
        <input type="text" v-model="name" placeholder="What your name" >
        <input type=file name="file" ref="photo">
        <button @click="uploadData">Upload</button>
      </p>
<!--    </form>-->
    <Modal></Modal>

    <UploadList></UploadList>

  </div>
</template>

<script>
    import UploadList from "../components/UploadList";
    import Modal from "../components/Modal";

    export default {
      name: "Upload",
      created() {
        document.title = "Upload new File";
      },
      data() {
        return {
            name: '',
            user: [],
        }
      },
      components:{
          UploadList,
          Modal,
      },
      methods: {
        async uploadData() {
            if (this.name !== "" && this.$refs.photo.files[0] !== undefined ) {
                let data = new FormData();
                let file = this.$refs.photo.files[0];

                data.append("name", this.name);
                data.append("image", file);
                // let res = await this.$axios.post('/api/upload/',data);
                // this.$store.commit('upload/addList',res);
                await this.$store.dispatch('upload/upload', {upload: 'http://localhost:8000/api/upload/', data: data});
                window.location.href = '/';
            }
            else{
                this.$store.commit('modal/setOpen');
            }

        },
      }
    }
</script>

<style scoped>


</style>
