<template>
  <div>
    <div class="wrap">
      <h2>Take picture</h2>
      <div class="web-camera-container">
        
        <div class="camera-button">
            <button type="button" class="button is-rounded" :class="{ 'is-primary' : !isCameraOpen, 'is-danger' : isCameraOpen}" @click="toggleCamera">
              <span v-if="!isCameraOpen">Open Camera</span>
              <span v-else>Close Camera</span>
          </button>
        </div>
        
        <div v-show="isCameraOpen && isLoading" class="camera-loading">
          <ul class="loader-circle">
            <li></li>
            <li></li>
            <li></li>
          </ul>
        </div>
        
        <div v-if="isCameraOpen" v-show="!isLoading" class="camera-box" :class="{ 'flash' : isShotPhoto }">
          <div class="camera-shutter" :class="{'flash' : isShotPhoto}"></div>
          <video v-show="!isPhotoTaken" ref="camera" :width="370" :height="337.5" autoplay></video>
          <canvas v-show="isPhotoTaken" id="photoTaken" ref="canvas" :width="370" :height="337.5"></canvas>
        </div>
        
        <div v-if="isCameraOpen && !isLoading" class="camera-shoot">
          <button type="button" class="button" @click="takePhoto">
            <img src="https://img.icons8.com/material-outlined/50/000000/camera--v2.png">
          </button>
        </div>
        
        <div v-if="isPhotoTaken && isCameraOpen" class="camera-download">
          <a id="downloadPhoto" download="my-photo.jpg" class="button" role="button" @click="downloadImage">
            Download
          </a>
        </div>
      </div>
      <div class="container">
      <!--UPLOAD-->
        <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
          <h2>Upload picture</h2>
          <div class="dropbox">
            <input type="file" multiple :name="uploadFieldName" :disabled="isSaving" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
              accept="image/*" class="input-file">
              <p v-if="isInitial">
                Drag your file(s) here to begin<br> or click to browse
              </p>
              <p v-if="isSaving">
                Uploading {{ fileCount }} files...
              </p>
          </div>
        </form>
        <!--SUCCESS-->
        <div v-if="isSuccess">
          <h2>Uploaded {{ uploadedFiles.length }} file(s) successfully.</h2>
          <p>
            <a href="javascript:void(0)" @click="reset()">Upload again</a>
          </p>
          <ul class="list-unstyled">
            <li v-for="item in uploadedFiles" v-bind="key='item'">
              <img :src="item.url" class="img-responsive img-thumbnail" :alt="item.originalName">
            </li>
          </ul>
        </div>
        <!--FAILED-->
        <div v-if="isFailed">
          <h2>Uploaded failed.</h2>
          <p>
            <a href="javascript:void(0)" @click="reset()">Try again</a>
          </p>
          <pre>{{ uploadError }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { wait, upload } from '../upload.js'
const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

export default {
  name: 'HelloWorld',
  data() {
      return {
        isCameraOpen: false,
        isPhotoTaken: false,
        isShotPhoto: false,
        isLoading: false,
        link: '#',
        uploadedFiles: [],
        uploadError: null,
        currentStatus: null,
        uploadFieldName: 'photos'
      }
    },
  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    }
  },
  methods: {
    toggleCamera() {
      if(this.isCameraOpen) {
        this.isCameraOpen = false;
        this.isPhotoTaken = false;
        this.isShotPhoto = false;
        this.stopCameraStream();
      } else {
        this.isCameraOpen = true;
        this.createCameraElement();
      }
    },
    
    createCameraElement() {
      this.isLoading = true;
      
      const constraints = (window.constraints = {
				audio: false,
				video: true
			});
			navigator.mediaDevices
				.getUserMedia(constraints)
				.then(stream => {
          this.isLoading = false;
					this.$refs.camera.srcObject = stream;
				})
				.catch(error => {
          this.isLoading = false;
					alert("May the browser didn't support or there is some errors.");
				});
    },
    stopCameraStream() {
      let tracks = this.$refs.camera.srcObject.getTracks();

			tracks.forEach(track => {
				track.stop();
			});
    },
    takePhoto() {
      if(!this.isPhotoTaken) {
        this.isShotPhoto = true;

        const FLASH_TIMEOUT = 50;

        setTimeout(() => {
          this.isShotPhoto = false;
        }, FLASH_TIMEOUT);
      }
      
      this.isPhotoTaken = !this.isPhotoTaken;
      
      const context = this.$refs.canvas.getContext('2d');
      context.drawImage(this.$refs.camera, 0, 0, 370, 337.5);
    },
    
    downloadImage() {
      const download = document.getElementById("downloadPhoto");
      const canvas = document.getElementById("photoTaken").toDataURL("image/jpeg")
    .replace("image/jpeg", "image/octet-stream");
      download.setAttribute("href", canvas);
    },
    reset() {
        // reset form to initial state
        this.currentStatus = STATUS_INITIAL;
        this.uploadedFiles = [];
        this.uploadError = null;
      },
      save(formData) {
        // upload data to the server
        this.currentStatus = STATUS_SAVING;
        upload(formData)
          .then(wait(1500)) // DEV ONLY: wait for 1.5s 
          .then(x => {
            this.uploadedFiles = [].concat(x);
            this.currentStatus = STATUS_SUCCESS;
          })
          .catch(err => {
            this.uploadError = err.response;
            this.currentStatus = STATUS_FAILED;
          });
      },
      filesChange(fieldName, fileList) {
        // handle file changes
        const formData = new FormData();
        if (!fileList.length) return;
        // append the files to FormData
        Array
          .from(Array(fileList.length).keys())
          .map(x => {
            formData.append(fieldName, fileList[x], fileList[x].name);
          });
        // save it
        this.save(formData);
      }
  },
  mounted() {
      this.reset();
  },
}
</script>

<style scoped>
.wrap {
  width: 380px;
  height: 820px;
  margin: 0;
  display: flex;
  flex-direction: column;
}

.web-camera-container {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  width: 120px;
}
    
.loader-circle {
  display: block;
  height: 14px;
  margin: 0 auto;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  transform: translateX(-50%);
  position: absolute;
  width: 100%;
  padding: 0;
}
li {
  display: block;
  float: left;
  width: 10px;
  height: 10px;
  line-height: 10px;
  padding: 0;
  position: relative;
  margin: 0 0 0 4px;
  background: #999;
  animation: preload 1s infinite;
  top: -50%;
  border-radius: 100%;
}
.dropbox {
    outline: 2px dashed grey; /* the dash box */
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    padding: 10px 10px;
    min-height: 200px; /* minimum height */
    position: relative;
    cursor: pointer;
  }
  
  .input-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 200px;
    position: absolute;
    cursor: pointer;
  }
  
  .dropbox:hover {
    background: lightblue; /* when mouse over to the drop zone, change color */
  }
  
  .dropbox p {
    font-size: 1.2em;
    text-align: center;
    padding: 50px 0;
  }


</style>
