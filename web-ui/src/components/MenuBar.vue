<template>
<div style="display: flex; flex-direction: column; justify-content: center;">
  <button class="button" v-on:click="clearDrawing">
    Clear Canvas
  </button>
  <textarea class="text-box" ref="text">
    Text
  </textarea>

  <button class="button" v-on:click="postText">
      Add Text
  </button>
</div>
</template>

<script>
import {clearDrawing, addText} from '@/api';

export default {
methods: {
  clearDrawing,
  addText,
  postText() {
    const text = this.$refs.text.value;
    // eslint-disable-next-line
    console.log(text);
    addText(text, 10, 10)
  }}
}
</script>

<style>
.text-box {
  margin-top: 5px;
  margin-bottom: 2px;
}
</style>
