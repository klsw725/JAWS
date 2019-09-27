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
    <Ring></Ring>

    <UploadList></UploadList>

  </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import UploadList from "../components/UploadList";
    import Modal from "../components/Modal";
    import Ring from "../components/Ring";

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
          Ring,
      },
      methods: {
        fileValidation(filename){
          var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
          if(!allowedExtensions.exec(filename)){
            alert('Please upload file having extensions .jpeg/.jpg/.png/.gif only.');
            return false;
          }else{
            return true;
          }
        },
        async uploadData() {
            let file = this.$refs.photo.files[0];
            if (this.name !== "" && file !== undefined ) {
              if (this.fileValidation(file.name)){
                this.$store.commit('ring/showRing');
                let data = new FormData();

                data.append("name", this.name);
                data.append("image", file);
                // let res = await this.$axios.post('/api/upload/',data);
                // this.$store.commit('upload/addList',res);
                let res = await this.$store.dispatch('upload/upload', {upload: 'http://localhost:8000/api/upload/', data: data});
                if(res == null){
                  alert('No Face Here');
                }
                this.$store.commit('ring/hideRing');
                window.location.href = '/';
              }
              else {
                window.location.href = '/';
              }

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
