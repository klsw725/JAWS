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
    <DashedSpinner v-if="ringState">얼굴 분석 중입니다</DashedSpinner>
    <UploadList></UploadList>

  </div>
</template>

<script>
    import {mapGetters} from 'vuex';
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
      computed: {
        ...mapGetters({
          ringState: 'upload/ringState',
        })
      },
      components:{
          UploadList,
          Modal,
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
            console.log(file);
            if (this.name !== "" && file !== undefined ) {
              if (this.fileValidation(file.name)){
                let data = new FormData();

                data.append("name", this.name);
                data.append("image", file);
                // let res = await this.$axios.post('/api/upload/',data);
                // this.$store.commit('upload/addList',res);
                await this.$store.dispatch('upload/upload', {upload: 'http://localhost:8000/api/upload/', data: data});
                // window.location.href = '/';
              }
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
