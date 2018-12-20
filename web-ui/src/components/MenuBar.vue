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
    <button class="button is-info" v-on:click="lock" v-if="!locked">
Lock
</button>
  <button class="button is-danger" v-on:click="unlock" v-if="locked">
Unlock
</button>
</div>
</template>

<script>
import {
  clearDrawing,
  lock,
  unlock,
  isLocked,
  addText
} from '@/api';

export default {
  data: () => ({
    locked: false
  }),
  methods: {
    clearDrawing,
    addText,
    lock,
    unlock,
    isLocked,
    postText() {
        const text = this.$refs.text.value;
        // eslint-disable-next-line
        console.log(text);
        addText(text, 10, 10)
    },
    async updateLockState() {
        this.locked = await isLocked();
    }
  },
  mounted() {
    setInterval(this.updateLockState, 1000);
  }
}
</script>

<style>
.text-box {
  margin-top: 5px;
  margin-bottom: 2px;
}
</style>
