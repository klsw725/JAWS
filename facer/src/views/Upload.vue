<template>
  <div>
    <Navigation></Navigation>
    <div class="container">
      <div class="row">
        <div class="col-lg-12 text-center">
          <h1 class="mt-5 title">Upload new File</h1>
          <div class="input-group">
            <input type="text" class="form-control" v-model="name" placeholder="What your name">
            <b-form-file placeholder="Choose a file or drop it here..." drop-placeholder="Drop file here..." v-model="photo" ref="photo" accept=".jpg, .png, .gif, .jpeg"></b-form-file>
<!--            <div class="custom-file">-->
<!--              <input type="file" class="custom-file-input" id="inputGroupFile02" name="file" ref="photo">-->
<!--              <label class="custom-file-label" for="inputGroupFile02" aria-describedby="inputGroupFileAddon02">Choose file</label>-->
<!--            </div>-->
            <div class="input-group-append">
              <button class="input-group-text" id="inputGroupFileAddon01"@click="uploadData">Upload</button>
            </div>
<!--            <input type=file name="file" ref="photo">-->

          </div>
        </div>
      </div>
    </div>
    <Modal></Modal>
    <Ring></Ring>

    <UploadList></UploadList>

  </div>
</template>

<script>
    import UploadList from "../components/UploadList";
    import Modal from "../components/Modal";
    import Ring from "../components/Ring";
    import Navigation from "../components/Navigation";

    export default {
      name: "Upload",
      created() {
        document.title = "Upload new File";
      },
      data() {
        return {
            name: '',
            photo:[],
        }
      },
      components:{
        Navigation,
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
            // let file = this.$refs.photo.files[0];
            if (this.name !== "" && this.photo !== undefined ) {
              if (this.fileValidation(this.photo.name)){
                this.$store.commit('ring/showRing');
                let data = new FormData();

                data.append("name", this.name);
                data.append("image", this.photo);
                // let res = await this.$axios.post('/api/upload/',data);
                // this.$store.commit('upload/addList',res);
                const token = localStorage.getItem("userInfo") ? JSON.parse(localStorage.getItem("userInfo")).token : null;
                let res = await this.$store.dispatch('upload/upload', {upload: 'http://localhost:8000/api/upload/', data: data, token: token});
                if(res.data['message']){
                  alert('No Face Here');
                }
                this.$store.commit('ring/hideRing');
                window.location.href = '/upload';
              }
              else {
                window.location.href = '/upload';
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
  .title{
    margin-bottom: 3%;
  }

</style>
