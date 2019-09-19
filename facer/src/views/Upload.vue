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
    <UploadList></UploadList>

  </div>
</template>

<script>
    import UploadList from "../components/UploadList";
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
      },
      methods: {
        async uploadData() {
          let data = new FormData();
          let file = this.$refs.photo.files[0];
          data.append("name", this.name);
          data.append("image", file);
          // let res = await this.$axios.post('/api/upload/',data);
          // this.$store.commit('upload/addList',res);
          await this.$store.dispatch('upload/upload', {upload: '/api/upload/', data: data});

        },
      }
    }
</script>

<style scoped>

</style>
