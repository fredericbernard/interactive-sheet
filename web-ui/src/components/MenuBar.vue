<template>
<div style="display: flex; flex-direction: column; justify-content: center;">
  <button class="button" v-on:click="clearDrawing">
    Clear Canvas
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
  isLocked
} from '@/api';

export default {
  data: () => ({
    locked: false
  }),
  methods: {
    clearDrawing,
    lock,
    unlock,
    isLocked,
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

</style>
